# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from extra import MORE, QUIZ, INTRO
from mods import MOD1
from mod4_bank import MOD4
from mod_auth import MOD_AUTH
from bank import T

_HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.join(_HERE, '..', 'src') if os.path.isdir(os.path.join(_HERE, '..', 'src')) and os.path.exists(os.path.join(_HERE, '..', 'src', 'm1.json')) else _HERE
m1 = json.load(open(os.path.join(SP, 'm1.json'), encoding='utf-8'))
m2 = json.load(open(os.path.join(SP, 'm2.json'), encoding='utf-8'))
DECK = {'m1': m1, 'm2': m2}

def paras(sh): return [p for p in sh.get('paras', [])]
def clean(s): return re.sub(r'\s+', ' ', s).strip()

def slide_titles(deck, s):
    # m1: sub = lesson title, title = chapter ; m2: sub = chapter, title = lesson
    return (s['sub'], s['title']) if deck == 'm1' else (s['title'], s['sub'])

def code_text(lines):
    out = [l.rstrip() if l.strip() else '' for l in lines]
    while out and not out[-1]: out.pop()
    return '\n'.join(out)

def cards_from(shapes):
    items, cur = [], None
    note = []
    for sh in shapes:
        n, p = sh['name'], [clean(x) for x in paras(sh) if clean(x)]
        if 'table' in sh: continue
        if not p and not (n.startswith('Código') or n.startswith('Exemplo') or n == 'Menu da aplicação'): continue
        if n.startswith('Título') or n.startswith('Rounded Rectangle'):
            cur = {'t': ' '.join(p), 'd': []}; items.append(cur)
        elif n.startswith('Código') or n.startswith('Exemplo') or n == 'Menu da aplicação':
            code = code_text(sh['paras'])
            if cur is None: cur = {'t': n, 'd': []}; items.append(cur)
            cur['code'] = code
        elif n.split(' ')[0] in ('Regra', 'Regras', 'Resumo', 'Nota', 'Conceitos', 'Aviso'):
            items.append({'t': '', 'd': p, 'note': True}); cur = None
        else:
            if cur is None: cur = {'t': n, 'd': []}; items.append(cur)
            cur['d'] += p
    return items

def split_lead(s):
    m = re.match(r'^([^.:]{2,28})[.:]\s+(.*)$', s)
    return {'lead': m.group(1), 'text': m.group(2)} if m else {'lead': '', 'text': s}

def lesson(deck, n, cid):
    s = DECK[deck][n - 1]
    t, _ = slide_titles(deck, s)
    names = {x['name']: x for x in s['shapes']}
    L = {'id': f'{deck}-{n}', 't': t}
    if 'Código C#' in names:
        L['type'] = 'code'
        L['code'] = code_text(names['Código C#']['paras'])
        L['points'] = [clean(x) for x in names['Pontos-chave']['paras'] if clean(x)]
        L['lang'] = 'xml' if L['code'].lstrip().startswith('<') else ('sh' if n in () else 'cs')
    elif t.startswith('Exercício prático') and 'Tabela' not in names:
        L['type'] = 'exercise'
        _t = t.replace('Exercício prático: ', ''); L['t'] = _t[:1].upper() + _t[1:]
        key = next(k for k in ('Lista de passos','Lista de exercícios','Histórias') if k in names)
        L['steps'] = [split_lead(clean(x)) for x in names[key]['paras'] if clean(x)]
        if 'Resultado esperado' in names:
            L['expected'] = code_text(names['Resultado esperado']['paras'])
        if 'Texto extra' in names:
            L['extra'] = clean(' '.join(names['Texto extra']['paras']))
    elif 'Tabela' in names:
        L['type'] = 'table'
        L['rows'] = names['Tabela']['table']
        L['note'] = clean(' '.join(names['Aviso tempos de vida']['paras'])) if 'Aviso tempos de vida' in names else ''
    else:
        L['type'] = 'cards'
        L['items'] = cards_from(s['shapes'])
    key = f'{deck}:{n}'
    if key in MORE: L['more'] = MORE[key]
    return L

def mk(deck, ranges, cid_prefix, titles):
    chapters = []
    for i, (title, rng) in enumerate(zip(titles, ranges), 1):
        cid = f'{cid_prefix}-{i}'
        chapters.append({'id': cid, 't': title, 'intro': INTRO[cid],
                         'lessons': [lesson(deck, n, cid) for n in rng],
                         'quiz': QUIZ.get(cid, [])})
    return chapters

# ------------------------------------------------------------ MODULE 2: C#
csharp_ch = mk('m1', [range(6, 20), range(21, 28), range(29, 41), range(42, 46)], 'csharp',
               ['Fundamentos da linguagem', 'Objetos e coleções', 'LINQ, exceções e async/await', 'Mini-aplicação de consola'])

# exercise 19: five independent exercises (not steps)
for L in csharp_ch[0]['lessons']:
    if L['id'] == 'm1-19':
        L['t'] = 'Cinco exercícios: tipos e fluxo'
        L['expected'] = None
        L['hint'] = 'Resolve o FizzBuzz primeiro. Os outros quatro podes fazê-los pela ordem que quiseres.'
# exercise 27: domain model
for L in csharp_ch[1]['lessons']:
    if L['id'] == 'm1-27':
        L['type'] = 'domain'
        L['t'] = 'Modelar o domínio'
        L['entities'] = [{'n': 'Policy', 'f': 'Number · Premium · Start'}, {'n': 'Policyholder', 'f': 'Customer · Since'}, {'n': 'Customer', 'f': 'Name · TaxId'}]
        L['rel'] = ['tem um', 'é um']
        L['steps'] = [{'lead': '', 'text': x} for x in ['Modelar Customer, Policy e Policyholder', 'Calcular o prémio com IPremiumCalculator', 'Guardar apólices numa List e numa Dictionary', 'Experimentar com três apólices de exemplo']]
        L['expected'] = 'Compila sem avisos\nTrês apólices criadas e listadas'
        L['more'] = dict(more='Policyholder (tomador) é o cliente que contrata a apólice. Neste modelo, Policyholder é um Customer (herança) e a Policy tem um Policyholder (composição). Aceitam-se variações, desde que as duas relações estejam corretas.', tryit='Desenha primeiro as três classes num papel com as setas «tem um» e «é um». Só depois escreve o código.')
# exercise 40
for L in csharp_ch[2]['lessons']:
    if L['id'] == 'm1-40': L['t'] = 'Cotações assíncronas'
# chapter 4: project statement with custom lesson ids
ch4 = csharp_ch[3]
for L in ch4['lessons']:
    if L['id'] == 'm1-45':
        L['type'] = 'cards'
        L['t'] = 'Antes de terminar'
        s = m1[44]
        crit = [clean(x['paras'][0]) for x in s['shapes'] if x['name'].startswith('Critério')]
        why = [clean(x) for x in [y for y in s['shapes'] if y['name'] == 'Perguntas'][0]['paras'] if clean(x)]
        L['items'] = [{'t': 'Critérios de conclusão', 'd': crit, 'check': True}, {'t': 'Perguntas de «porquê»', 'd': why}]
ch4['lessons'][0]['more'] = dict(more='Tudo fica em memória enquanto o programa corre: não há base de dados neste módulo. Decide tu a ordem em que implementas as opções do menu. Uma sugestão: começa pela 1 e pela 2, porque a 3 depende de ter apólices criadas.', tryit='Antes de escreveres código, desenha as classes que vais precisar e a estrutura de dados onde guardas as apólices.')
ch4['lessons'][2]['more'] = dict(more='Reproduz o exemplo exatamente, incluindo o formato do prémio com duas casas e vírgula decimal. Os extras são opcionais, mas o de impedir NIFs repetidos obriga-te a pensar num Dictionary.')
ch4['lessons'][3]['more'] = dict(more='O critério de explicar uma classe e uma consulta LINQ do teu código é o mais importante: mostra que percebes o que escreveste.')

csharp_outro = dict(
    done=[clean(x) for x in m1[45]['shapes'][1]['paras']],
    docs=[{'t': 'Documentação oficial de C#', 'u': 'https://learn.microsoft.com/dotnet/csharp/'},
          {'t': 'Visita guiada ao C#', 'u': 'https://learn.microsoft.com/dotnet/csharp/tour-of-csharp/'},
          {'t': 'Referência da linguagem', 'u': 'https://learn.microsoft.com/dotnet/csharp/language-reference/'}],
    practice=[clean(x) for x in m1[45]['shapes'][5]['paras']])
MOD2 = dict(id='csharp', num=2, kind='course', title='C#', short='C#',
            tagline='A linguagem de base: tipos, objetos, coleções, LINQ, erros e async/await, até uma aplicação de consola completa.',
            chapters=csharp_ch, outro=csharp_outro)

# ------------------------------------------------------------ MODULE 3: .NET
dn_ch = mk('m2', [range(7, 12), range(13, 25), range(26, 32), range(33, 45), range(46, 53), range(54, 62)], 'dotnet',
           ['A plataforma .NET', 'ASP.NET Core e Web API', 'Dependency Injection', 'Entity Framework Core', 'Testes unitários', 'Organização do código'])
# merge endpoint table (slide 24) into exercise 23
ch2 = dn_ch[1]
ex23 = [L for L in ch2['lessons'] if L['id'] == 'm2-23'][0]
ex24 = [L for L in ch2['lessons'] if L['id'] == 'm2-24'][0]
ex23['table'] = ex24['rows']
ex23['expected'] = None
ch2['lessons'] = [L for L in ch2['lessons'] if L['id'] != 'm2-24']
# clean exercise 11 (the deck text for the first two steps is cut)
for L in dn_ch[0]['lessons']:
    if L['id'] == 'm2-11':
        L['steps'] = [split_lead(x) for x in [
            'Criar a solução: Insurance, com o projeto Api (webapi)',
            'Adicionar à solução: Domain (classlib) e Tests (xunit)',
            'Referenciar: o Domain na Api e a Api nos Tests',
            'Instalar um pacote na Api via NuGet: Newtonsoft.Json',
            'Compilar e correr: a Api e abrir o endereço indicado no terminal']]
        L['more'] = dict(more='Faz tudo na linha de comandos, sem o assistente do IDE: assim ficas a saber exatamente o que cada comando cria. Tabela de equivalências com o Visual Studio está no tema «Soluções e Projetos».', tryit='Corre tree (ou tree /f) para ver a estrutura de pastas e explica o que cada projeto vai ter.')
for ch in dn_ch:
    for L in ch['lessons']:
        if L['type'] == 'exercise' and 'more' not in L and L.get('extra'):
            L['more'] = dict(more='Só passas ao capítulo seguinte quando o resultado esperado aparecer no teu computador. Se algo falhar, lê a mensagem de erro de baixo para cima: a última linha costuma dizer o que correu mal.', tryit=L['extra'])
dotnet_outro = dict(
    done=[clean(x) for x in m2[61]['shapes'][1]['paras']],
    docs=[{'t': 'Documentação do .NET', 'u': 'https://learn.microsoft.com/dotnet/'},
          {'t': 'ASP.NET Core', 'u': 'https://learn.microsoft.com/aspnet/core/'},
          {'t': 'Entity Framework Core', 'u': 'https://learn.microsoft.com/ef/core/'},
          {'t': 'xUnit', 'u': 'https://xunit.net/'}],
    practice=[clean(x) for x in m2[61]['shapes'][5]['paras']])
MOD3 = dict(id='dotnet', num=3, kind='course', title='.NET', short='.NET',
            tagline='A plataforma, a Web API, Dependency Injection, base de dados, testes e organização em camadas.',
            chapters=dn_ch, outro=dotnet_outro)


# ---- structural patches
ALL = {L['id']: L for m in (MOD2, MOD3) for c in m['chapters'] for L in c['lessons']}
for k, n in {'m2-7': 5, 'm2-14': 5, 'm2-33': 3, 'm2-34': 3, 'm2-60': 5}.items(): ALL[k]['flow'] = n
ALL['m2-46'].update(type='pyramid', items=[
    {'t': 'Unitário', 'd': ['Uma classe ou método isolado, sem base de dados nem rede.']},
    {'t': 'Integração', 'd': ['Várias peças reais juntas, como a API e a base de dados.']},
    {'t': 'Ponta a ponta', 'd': ['O sistema completo, como um utilizador o usa.']}],
    levels=[{'n': 'Ponta a ponta', 'd': 'poucos, lentos'}, {'n': 'Integração', 'd': 'alguns'}, {'n': 'Unitários', 'd': 'muitos, rápidos'}])
ALL['m2-55'].update(type='layers', rules=['As dependências apontam para dentro.', 'O Domínio não conhece o EF Core nem o ASP.NET Core.', 'As interfaces ficam dentro; as implementações, fora.'],
    levels=[{'n': 'Infraestrutura e API', 'd': 'EF Core, HTTP'}, {'n': 'Aplicação', 'd': 'casos de uso'}, {'n': 'Domínio', 'd': 'entidades e regras'}])
ALL['m2-55']['more'] = dict(more='Imagina círculos concêntricos. No centro estão as regras do negócio, que mudam pouco. Nas camadas de fora estão os detalhes técnicos (base de dados, HTTP), que mudam mais. Uma camada só pode conhecer as que estão mais para dentro.\n\nO truque que torna isto possível é a inversão de dependência: a Application declara a interface IPolicyRepository e a Infrastructure implementa-a. No Módulo 4 constróis exatamente isto.', tryit='Pergunta a ti próprio, para cada classe que escreves: em que círculo vive? E o que é que ela precisa de conhecer?')
ALL['m2-60']['more'] = dict(more='Segue o pedido de um POST /api/policies: o controller converte HTTP em comando, o handler decide, o repositório guarda e a resposta faz o caminho inverso. Cada passo tem uma só responsabilidade, por isso podes testar e alterar cada um sem mexer nos outros.', tryit='Abre o Módulo 4 e usa o explorador «Percurso de um pedido» para ver este caminho com código real.')
ALL['m2-54']['more'] = dict(more='Um controller que valida, calcula o prémio e fala com a base de dados faz três trabalhos. Para o testar tens de ter base de dados; para trocar a base de dados mexes no controller. Dividir em camadas dá a cada parte um motivo único para mudar.')
ALL['m2-58']['more'] = dict(more='CQRS (Command Query Responsibility Segregation) separa quem altera de quem lê. Aqui aplica-se na forma simples: classes pequenas, uma por caso de uso. Não é preciso nenhuma biblioteca. Se um dia a equipa adotar uma biblioteca de mediação, confirma primeiro a licença.')
ALL['m2-26']['more'] = dict(more='À esquerda, PolicyService cria BasicPremium com new: está presa a essa classe e não podes testá-la com outra. À direita recebe IPremiumCalculator pelo construtor: quem cria o PolicyService decide qual usar. É a mesma ideia da composição que viste em C#.', tryit='Cria um FakePremium que devolve sempre 1 e passa-o ao PolicyService num teste.')
ALL['m2-14']['more'] = dict(more='O pipeline é uma cadeia: cada middleware pode responder logo (por exemplo, rejeitar um pedido sem autenticação) ou passar ao seguinte. Quando o controller devolve a resposta, esta volta pela mesma cadeia, ao contrário. É por isso que a ordem no Program.cs importa.')
ALL['m2-21']['more'] = dict(more='Numa API REST, o URL é um substantivo (o recurso) e o verbo HTTP é a ação: GET lê, POST cria, PUT/PATCH altera, DELETE apaga. Em RPC, o URL é um verbo (calculatePremium) e quase tudo é POST. REST é a escolha por omissão para os recursos do domínio; RPC aparece em operações que não são um recurso, como «calcular».')
ALL['m2-9']['more'] = dict(more='A linha de comandos e o Visual Studio fazem o mesmo. A linha de comandos é mais rápida de repetir, fica em scripts e funciona em qualquer IDE. Sabê-la é o que te permite ajudar num pipeline de Release, onde não há IDE.')
ALL['m2-18']['more'] = dict(more='Os códigos agrupam-se por centena: 2xx sucesso, 4xx erro do cliente (corrige o pedido), 5xx erro do servidor (a culpa não é do cliente). Escolher o código certo poupa horas de depuração a quem consome a tua API.', tryit='Antes de abrires a coluna «Quando», tenta adivinhar o código para cada situação.')
ALL['m2-43']['more'] = dict(more='O N+1 acontece quando carregas uma lista (1 consulta) e depois acedes a uma relação de cada item (N consultas). Include resolve com um JOIN. ToList antes do Where traz tudo para memória. Estes dois erros não dão exceção: só se notam na lentidão, por isso convém olhar para o SQL gerado (LogTo ou o log do EF).')
ALL['m2-51']['more'] = dict(more='Method_Scenario_Result, por exemplo Calculate_NewCustomer_ReturnsBasePremium. Quando este teste falhar no CI, o nome já diz o que se partiu, sem abrir o código.')
ALL['m2-30']['more'] = dict(more='Um construtor com sete parâmetros é um sinal: a classe provavelmente faz demasiado. GetService dentro do código (service locator) esconde as dependências e dificulta os testes. O construtor é o sítio honesto para declarar do que a classe precisa.')
ALL['m2-8']['tryit_cmd'] = 'dotnet --list-sdks'

# ---- domain switch: insurance -> bank
MOD1, MOD2, MOD3 = T(MOD1), T(MOD2), T(MOD3)
ALL = {L['id']: L for m in (MOD2, MOD3) for c in m['chapters'] for L in c['lessons']}
def sub(lid, a, b):
    L = ALL[lid]
    for k in ('code', 'expected', 'extra', 'hint'):
        if isinstance(L.get(k), str) and a in L[k]: L[k] = L[k].replace(a, b)
    for it in L.get('items', []):
        if it.get('code'): it['code'] = it['code'].replace(a, b)
        it['d'] = [x.replace(a, b) for x in it.get('d', [])]
    for st in L.get('steps', []):
        st['text'] = st['text'].replace(a, b)
    if L.get('more') and a in (L['more'].get('more') or ''): L['more']['more'] = L['more']['more'].replace(a, b)
    return L
def code(lid, text): ALL[lid]['code'] = text.strip('\n')

code('m1-12', """static string Season(int month) => month switch
{
    12 or 1 or 2 => "winter",
    >= 6 and <= 8 => "summer",
    _ => "other season"
};

decimal bonus = (years, vip) switch
{
    (>= 10, true) => 0.020m,
    (>= 10, false) => 0.015m,
    _ => 0m
};""")
code('m1-18', """static decimal CalculateBonus(int customerYears)
{
    if (customerYears >= 10) return 0.015m;
    if (customerYears >= 5) return 0.010m;
    return 0m;
}

static int Add(int a, int b = 0) => a + b;

var b = CalculateBonus(6);   // 0.010""")
code('m1-23', """public interface IInterestCalculator
{
    decimal Calculate(Account account);
}

public class StandardInterest : IInterestCalculator
{
    public decimal Calculate(Account a) => a.Balance * 0.01m;
}

public class PromoInterest : IInterestCalculator
{
    private readonly decimal _rate;
    public PromoInterest(decimal rate) => _rate = rate;
    public decimal Calculate(Account a)
        => a.Balance * _rate;
}""")
code('m1-24', """public class InterestService
{
    private readonly IInterestCalculator _calculator;

    // composition: receives the calculator from outside
    public InterestService(IInterestCalculator calculator)
        => _calculator = calculator;

    public decimal Annual(Account a)
        => _calculator.Calculate(a);
}

var normal = new InterestService(new StandardInterest());
var promo = new InterestService(new PromoInterest(0.03m));""")
sub('m1-16', 'With VAT: {balance * 1.23m}', 'With interest: {balance * 1.02m}')
sub('m1-33', 'a.Balance <= 0', 'a.Balance < 0'); sub('m1-33', '"Balance <= 0"', '"Balance < 0"')
L = ALL['m1-19']
L['steps'][3] = {'lead': 'Juros com bónus', 'text': 'Calcula os juros anuais de uma conta, aplicando um bónus à taxa que depende dos anos de cliente.'}
ALL['m1-27']['steps'][1]['text'] = 'Calcular os juros com IInterestCalculator'
ALL['m1-27']['entities'][0]['f'] = 'Number · Balance · Opened'
L = ALL['m1-40']
L['t'] = 'Saldos das contas'
L['steps'] = [split_lead(x) for x in [
    'Exceção própria: BalanceUnavailableException, com o número da conta.',
    'Saldo assíncrono: GetBalanceAsync demora 200 ms e lança a exceção se o número terminar em 9.',
    'Em paralelo: Pedir o saldo de todas as contas com Task.WhenAll.',
    'Falhas isoladas: Uma conta sem resposta não pode deitar abaixo as outras.',
    'LINQ: Somar os saldos obtidos e listar as contas sem resposta.']]
L['expected'] = 'AC-001: 332,28\nAC-002: 332,28\nAC-009: indisponível\n\nTotal: 664,56\nSem resposta: AC-009'
sub('m1-42', 'o nome e o NIF do cliente e o saldo.', 'o nome e o NIF do cliente e o saldo inicial.')
sub('m1-42', 'da mais cara para a mais barata', 'do maior para o menor')
sub('m2-20', '[Range(0.01, 1000000)]', '[Range(0, 1000000)]')
sub('m1-43', 'O saldo é um número maior que zero.', 'O saldo inicial é um número maior ou igual a zero.')
sub('m1-44', 'Saldo: 320,50', 'Saldo inicial: 320,50')
sub('m1-44', 'Aplicar um desconto com a interface IInterestCalculator.', 'Calcular os juros com a interface IInterestCalculator.')
sub('m2-16', '"MaxBonus": 0.2', '"MaxBonus": 0.02')
for it in ALL['m2-26']['items']:
    if it.get('code'): it['code'] = it['code'].replace('decimal Total(', 'decimal Interest(')
L = ALL['m2-31']
L['t'] = 'Juros injetados'
L['steps'] = [split_lead(x) for x in [
    'Contrato. IInterestCalculator, com as implementações StandardInterest e PromoInterest',
    'Registar. a implementação no Program.cs com AddScoped',
    'Injetar. o calculador num AccountService e usá-lo no POST para devolver os juros anuais',
    'Configurar. a taxa em appsettings.json, lida com IOptions',
    'Registar no log. o número da conta e os juros calculados com ILogger']]
L['expected'] = 'POST /api/accounts\n{ "balance": 1000.00 }\n\n201 Created\n{\n  "number": "AC-001",\n  "annualInterest": 20.00\n}'
L['extra'] = 'Escolher a implementação por configuração (Standard ou Promo) sem recompilar.'
code('m2-47', """public class PromoInterestTests
{
    [Fact]
    public void Calculate_Rate2Percent_Returns2PercentOfBalance()
    {
        // Arrange
        var calc = new PromoInterest(0.02m);
        var acc = new Account("AC-001", ana, 200m);

        // Act
        var result = calc.Calculate(acc);

        // Assert
        Assert.Equal(4m, result);
    }
}""")
code('m2-48', """[Theory]
[InlineData(0, 200, 0)]
[InlineData(2, 200, 4)]
[InlineData(5, 200, 10)]
public void Calculate_AppliesRate(
    int ratePercent, int balance, int expected)
{
    var calc = new PromoInterest(ratePercent / 100m);
    var acc = new Account("AC-001", ana, balance);

    Assert.Equal(expected, calc.Calculate(acc));
}""")
code('m2-50', """var repo = Substitute.For<IAccountRepository>();
repo.GetAsync("AC-001")
    .Returns(new Account("AC-001", ana, 200m));

var service = new AccountService(
    repo, new PromoInterest(0.02m));

var interest = await service.CalculateAsync("AC-001");

Assert.Equal(4m, interest);
await repo.Received(1).GetAsync("AC-001");""")
L = ALL['m2-52']
L['steps'] = [split_lead(x) for x in [
    'Três testes. [Fact] para PromoInterest: taxa 0%, 2% e 5%',
    'Um Theory. com [InlineData] para os mesmos cálculos',
    'Uma exceção. InvalidAccountException para um saldo negativo',
    'Um mock. do repositório para testar o AccountService']]
sub('m2-44', 'precisão do Balance', 'precisão do Balance')
# my own explanation texts
MORE_FIX = {
 'm1-6': ('Num sistema de seguros, esse erro de arredondamento aparece em prémios e comissões.', 'Num banco, esse erro de arredondamento aparece em saldos, juros e comissões.'),
}
ALL['m1-6']['more']['pit'] = '0.1 + 0.2 == 0.3 devolve false com double. Num banco, esse erro de arredondamento aparece em saldos, juros e comissões.'
ALL['m2-51']['more']['more'] = ALL['m2-51']['more']['more'].replace('Calculate_NewCustomer_ReturnsBaseBalance', 'Calculate_PromoRate_ReturnsInterest')
ALL['m2-54']['more']['more'] = ALL['m2-54']['more']['more'].replace('calcula o saldo', 'calcula os juros')
ALL['m1-12']['more']['tryit'] = 'Escreve um switch expression que devolve o bónus da taxa de juro (0, 0.5%, 1%) consoante os anos de cliente, com intervalos.'
ALL['m1-18']['more']['tryit'] = 'Cria CalculateInterest(decimal balance, decimal bonus = 0m) e chama-o com e sem bónus, com o parâmetro nomeado.'


# ---- .NET 10: OpenAPI is built in, Swagger UI is a separate package
ALL['m2-22'].update(t='Documentar com OpenAPI e Swagger UI', lang='cs',
  code="""// 1. the document: built into ASP.NET Core (the template already has it)
builder.Services.AddOpenApi();

// 2. the UI: a separate package
// dotnet add package Swashbuckle.AspNetCore.SwaggerUI

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();   // serves /openapi/v1.json
    app.UseSwaggerUI(o =>
        o.SwaggerEndpoint("/openapi/v1.json", "v1"));   // /swagger
}""",
  points=['OpenAPI é o documento que descreve o contrato da API: endpoints, parâmetros e respostas.',
          'Desde o .NET 9, o ASP.NET Core gera esse documento sozinho (Microsoft.AspNetCore.OpenApi).',
          'O template deixou de incluir o Swashbuckle e, no .NET 10, o documento é OpenAPI 3.1.',
          'A página para experimentar é uma peça à parte: o pacote Swashbuckle.AspNetCore.SwaggerUI.'])
ALL['m2-22']['more'] = dict(
  more='São duas peças diferentes. O documento OpenAPI (o JSON em /openapi/v1.json) é gerado pelo próprio ASP.NET Core com AddOpenApi e MapOpenApi. A página interativa (o Swagger UI) só desenha esse documento: não o gera.\n\nAntes do .NET 9, o template incluía o Swashbuckle, que fazia as duas coisas. Agora o documento é nativo e, se quiseres a página do Swagger UI, acrescentas o pacote Swashbuckle.AspNetCore.SwaggerUI e apontas-o para o documento. Existem outras interfaces que leem o mesmo documento (Scalar, ReDoc), por isso trocar de UI não mexe na API.\n\nO .NET 10 passou o documento para OpenAPI 3.1 por omissão. Se algum cliente ou ferramenta não o suportar, podes fixar a versão 3.0 nas opções do AddOpenApi.',
  pit='Abrir /swagger e receber 404. Sem o pacote SwaggerUI, ou fora do ambiente Development, a página não existe, mas o documento /openapi/v1.json continua a funcionar.',
  tryit='Abre primeiro /openapi/v1.json e depois /swagger. Executa um POST e vê o 201 com o cabeçalho Location.')

# ---- module numbering: Autenticação is module 4, the project becomes module 5
def _renum(o):
    if isinstance(o, str): return o.replace('Módulo 4', 'Módulo 5')
    if isinstance(o, list): return [_renum(x) for x in o]
    if isinstance(o, dict): return {k: _renum(v) for k, v in o.items()}
    return o
MOD1, MOD2, MOD3 = _renum(MOD1), _renum(MOD2), _renum(MOD3)
_ac = MOD1['sections'][1]['blocks']
for _b in _ac:
    if _b.get('k') == 'outcomes':
        _it = _b['items']
        _it.insert(2, dict(mod='auth', t='Proteger uma API', d='A diferença entre Basic Auth e OAuth 2.0, como funciona um JWT e como emitir, validar e autorizar com tokens.',
            more=dict(more='Resultado verificável: uma API pequena que faz login, emite um JWT, protege endpoints e distingue clientes de gestores, testada com o Bruno.')))
        _it[3]['d'] = 'Uma API de um banco com Clean Architecture, construída de raiz: dois dias guiados e depois um enunciado com mais funcionalidades do que as que cabem no tempo, para planeares e escolheres.'
        _it[3]['more'] = dict(more='Resultado verificável: uma solução com cinco projetos, migrations, autenticação JWT, as funcionalidades que escolheste no teu plano, tratamento de erros por middleware e testes aos handlers.')
for _s in MOD1['sections']:
    for _b in _s['blocks']:
        if _b.get('k') == 'software': _b['items'] = [i for i in _b['items'] if i['id'] not in ('docker', 'stack')]
        if _b.get('k') in ('steps', 'cards'): _b['items'] = [i for i in _b['items'] if i['t'] != 'Pesquisar']
        if _b.get('k') == 'p':
            _b['t'] = _b['t'].replace('Quatro módulos', 'Cinco módulos')
            _b['t'] = _b['t'].replace('passas para a plataforma .NET e terminas com uma API completa', 'passas para a plataforma .NET, aprendes a proteger uma API e terminas com um projeto completo')
        if _b.get('k') == 'software':
            for _i in _b['items']:
                if _i['id'] == 'api':
                    _i['name'] = 'Bruno'
                    _i['why'] = 'Enviar pedidos HTTP à tua API e guardá-los numa coleção, em ficheiros de texto que podes pôr no repositório.'
                    _i['expect'] = 'Consegues enviar um GET a qualquer URL público.'
                    _i['install'] = 'usebruno.com. Não instales o Postman: usamos só o Bruno.'
                    _i['more'] = dict(more='O Bruno guarda as coleções em ficheiros de texto (.bru), que revês em Pull Requests como qualquer código. Importa o documento OpenAPI da tua API para criares a coleção. Usa-se no módulo de Autenticação e no projeto final.')


# ---- editorial review (voz-bruno-pt): no colon-contrasts, AO spelling, English technical terms
FIXES = [
 ('Postman ou Bruno servem para coleções de pedidos.', 'O Bruno serve para criar coleções de pedidos.'),
 ('O Bruno é uma alternativa ao Postman: guarda a coleção', 'O Bruno guarda a coleção'),
 (', ou um container Docker com a imagem do SQL Server.', '.'),
 (' Se usares Docker, a porta e a password são as que definires no container.', ''),
 ('O IL não é código máquina: é igual em Windows, Linux e macOS.', 'O IL não é código máquina e, por isso, é igual em Windows, Linux e macOS.'),
 ('O refresh token não é um JWT: é um valor aleatório que só tem significado no teu servidor.', 'O refresh token não é um JWT mas sim um valor aleatório, que só tem significado no teu servidor.'),
 ('O objetivo não é acertar, é aprender a estimar e a ajustar o plano quando a realidade o contradiz.', 'O objetivo não é só acertar, mas também aprender a estimar e a ajustar o plano quando a realidade o contradiz.'),
 ('?. pára se o valor for null.', '?. para se o valor for null.'),
 ('o pedido pára aqui', 'o pedido para aqui'),
 ('Porque é que Conta é um record?', 'Porque é que Account é um record?'),
 ('Base da injeção de dependências.', 'Base da Dependency Injection.'),
 ('Postman e Bruno importam o mesmo documento para criar coleções de pedidos.', 'O Bruno importa o mesmo documento para criar coleções de pedidos.'),
]
def _fixall(o):
    if isinstance(o, str):
        for a, b in FIXES: o = o.replace(a, b)
        return o
    if isinstance(o, list): return [_fixall(x) for x in o]
    if isinstance(o, dict): return {k: _fixall(v) for k, v in o.items()}
    return o
MOD4['phases'].sort(key=lambda p: p['id'] != 'p4')   # the intro with the trainer goes first
MOD4['extras'] = [x for x in MOD4['extras'] if 'Dockerfile' not in x]
from m4_stories import US, EPICS
_ep = {f: e for e in EPICS for f in e['fs']}
for _p in MOD4['phases']:
    for _f in _p.get('features', []):
        if _f['id'] in US:
            _f['us'] = US[_f['id']]; _f['epic'] = _ep[_f['id']]['id']
    if _p.get('features'):
        _p['epics'] = [dict(id=e['id'], t=e['t'], d=e['d']) for e in EPICS]
        _p['features'].sort(key=lambda f: [x['id'] for x in EPICS].index(f['epic']) * 100 + _ep[f['id']]['fs'].index(f['id']) if f.get('epic') else 9999)
_ep_rows = MOD4['closing'].get('endpoints') if isinstance(MOD4.get('closing'), dict) else None
_rows = MOD4.get('endpoints')
if _rows:
    _hdr, _body = _rows[0], _rows[1:]
    _g = [r for r in _body if r[0] == 'Guia']; _f = [r for r in _body if r[0] != 'Guia']
    _f.sort(key=lambda r: int(r[0][1:]))
    MOD4['endpoints'] = [_hdr] + _g + _f
MOD1, MOD2, MOD3, MOD_AUTH, MOD4 = [_fixall(m) for m in (MOD1, MOD2, MOD3, MOD_AUTH, MOD4)]
# ---- new modules authored as JSON in content/modules/ (see docs/AUTHORING.md)
import glob
from validate import validate_module
EXTRA_MODS = []
_cdirs = [os.path.join(_HERE, 'content', 'modules'), os.path.join(_HERE, '..', 'content', 'modules')]
for _d in _cdirs:
    for _f in sorted(glob.glob(os.path.join(_d, '*.json'))):
        if os.path.basename(_f).startswith('_'): continue
        _m = json.load(open(_f, encoding='utf-8'))
        _errs = validate_module(_m, os.path.basename(_f))
        if _errs:
            print('INVALID MODULE', _f); [print('  -', e) for e in _errs]; sys.exit(1)
        EXTRA_MODS.append(_m)
    if EXTRA_MODS: break
_mods = [MOD1, MOD2, MOD3, MOD_AUTH] + EXTRA_MODS + [MOD4]
for _i, _m in enumerate(_mods, 1): _m['num'] = _i
DATA = {'modules': _mods}

def build():
    here = os.path.dirname(__file__)
    tpl = open(os.path.join(here, 'tpl.html'), encoding='utf-8').read()
    data = json.dumps(DATA, ensure_ascii=False).replace('</', '<\\/')
    tpl = tpl.replace('/*DATA*/null', data)
    p1, p2 = tpl.split('<!--BODY-->')
    out = None
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    if not out: open(os.path.join(here, 'artifact.html'), 'w', encoding='utf-8').write(p1 + p2)
    head = '<!doctype html>\n<html lang="pt-PT">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    open(out or os.path.join(here, 'academia-dotnet.html'), 'w', encoding='utf-8').write(head + p1 + '\n</head>\n<body>\n' + p2 + '\n</body>\n</html>\n')
    print('ok', len(tpl))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'dump':
        json.dump(DATA, open(os.path.join(os.path.dirname(__file__), 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    else:
        build()
