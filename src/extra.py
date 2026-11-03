# -*- coding: utf-8 -*-
# Handwritten "Saber mais" content, quizzes and chapter intros. Keys: "<deck>:<slide number>".

MORE = {
# ---------------- C# · Fundamentos ----------------
"m1:6": dict(
 more="Em C# cada variável tem um tipo fixo, decidido em compilação. Os tipos de valor (int, decimal, bool) guardam o próprio valor; os de referência (string, classes) guardam um apontador para o objeto. Na prática, isto muda o que acontece quando copias uma variável ou a passas a um método.\n\nOs tipos double e float guardam números em binário e não conseguem representar 0.1 exatamente. O decimal trabalha em base 10, por isso é o tipo certo para dinheiro. O sufixo m em 320.50m diz ao compilador que o literal é decimal.",
 pit="0.1 + 0.2 == 0.3 devolve false com double. Num sistema de seguros, esse erro de arredondamento aparece em prémios e comissões.",
 tryit="Antes de correres o código, escreve o tipo que esperas para total. Depois passa o rato por cima de var no IDE e confirma."),
"m1:7": dict(
 more="A divisão entre dois inteiros é inteira: 7 / 2 dá 3. Para obter 3.5, pelo menos um dos operandos tem de ser decimal ou double. O operador % devolve o resto e é útil para testar múltiplos (é a base do FizzBuzz).\n\nOs operadores && e || são de curto-circuito: se o lado esquerdo já decide o resultado, o direito nem é avaliado. Isso permite escrever user != null && user.IsActive sem rebentar.",
 pit="Dividir inteiros e esperar um decimal. Converter o resultado depois da divisão já é tarde demais.",
 tryit="Calcula 7 / 2, 7 % 2 e 7m / 2 e compara os três resultados."),
"m1:8": dict(
 more="Desde o C# 8, o compilador distingue string (nunca null) de string? (pode ser null) quando o projeto tem Nullable ativo. Os operadores de null existem para lidar com isto sem encher o código de ifs.\n\n?. devolve null em vez de lançar NullReferenceException. ?? dá um valor alternativo. ??= atribui só quando a variável ainda é null, o que é prático para valores por omissão.",
 pit="Usar ! (null-forgiving) para calar um aviso. O aviso estava a proteger-te de um erro em execução.",
 tryit="Declara string? email = null; e escreve email?.ToUpper() ?? \"n/a\". Troca o valor para \"a@b.pt\" e vê a diferença."),
"m1:9": dict(
 more="O operador ternário c ? a : b é uma expressão: devolve um valor, por isso pode ser usado dentro de uma atribuição ou de uma interpolação. Se a condição precisa de mais de duas ramificações, um switch expression fica mais legível.\n\nO operador is faz pattern matching: testa o tipo e, no mesmo passo, declara uma variável já convertida (obj is Policy p). Os padrões and, or e not permitem escrever intervalos como age is >= 18 and < 65.",
 pit="Encadear ternários dentro de ternários. Passados dois níveis, troca por um switch expression.",
 tryit="Escreve um método que recebe object e devolve texto diferente para int, string e Policy usando is."),
"m1:10": dict(
 more="O if avalia sempre um bool. Em C# não existe a conversão implícita de números ou objetos para bool, o que evita erros do tipo if (x = 5).\n\nA técnica de retornar cedo (guard clauses) trata primeiro os casos inválidos e sai do método. O caminho feliz fica no fim, sem aninhamento.",
 pit="Omitir as chavetas num bloco de várias linhas. Só a primeira linha pertence ao if.",
 tryit="Reescreve um if/else aninhado com três níveis usando retornos antecipados."),
"m1:11": dict(
 more="O switch clássico compara uma variável com vários valores. Cada case tem de terminar com break ou return; o C# não permite o 'fall through' acidental de outras linguagens. Cases seguidos sem código partilham o mesmo resultado.",
 pit="Esquecer o default. Se aparecer um valor inesperado, o programa segue em frente sem fazer nada.",
 tryit="Mapeia o código de um estado (1, 2, 3) para o texto 'Ativa', 'Cancelada', 'Suspensa' e testa com um valor fora do intervalo."),
"m1:12": dict(
 more="O switch expression devolve um valor e usa => em vez de case/break. Cada braço é um padrão, o que permite relacionais (< 18), combinações (and/or) e propriedades. O _ funciona como default. Se nenhum braço cobrir o valor, o compilador avisa.",
 tryit="Escreve um switch expression que devolve o desconto (0, 5%, 10%) consoante os anos de cliente, com intervalos."),
"m1:13": dict(
 more="foreach percorre qualquer coleção sem expor índices, o que elimina erros de 'um a mais' ou 'um a menos'. O for é a ferramenta quando precisas do índice ou de um passo diferente de 1.\n\nAlterar a coleção durante um foreach lança InvalidOperationException. Se precisas de remover elementos, constrói uma nova lista ou usa RemoveAll.",
 pit="Remover elementos de uma List dentro de um foreach sobre a própria List."),
"m1:14": dict(
 more="while testa a condição antes de cada volta, por isso pode não correr nenhuma vez. do-while testa no fim e corre pelo menos uma: é a escolha natural para menus e para pedir um valor até ser válido.\n\nbreak sai do ciclo; continue salta para a volta seguinte.",
 pit="Ciclos infinitos por esquecer de atualizar a variável da condição.",
 tryit="Escreve um menu em do-while que só termina quando o utilizador escolhe 0."),
"m1:15": dict(
 more="As strings em .NET são imutáveis: cada + cria uma string nova. Para três ou quatro junções não faz diferença. Num ciclo com milhares de iterações, o StringBuilder evita criar milhares de strings intermédias.\n\nstring.Join junta uma coleção com um separador sem teres de tratar o último elemento à parte.",
 tryit="Junta os números de 1 a 5 com string.Join(\", \", ...)."),
"m1:16": dict(
 more="A interpolação $\"...\" é a forma preferida de construir texto. Dentro das chavetas podes usar qualquer expressão, incluindo chamadas de métodos e ternários (entre parênteses). As raw strings com três aspas dispensam escapes e são ideais para JSON e SQL de teste.",
 pit="Esquecer o $ no início e ver as chavetas escritas literalmente no ecrã."),
"m1:17": dict(
 more="Dentro da interpolação, o formato vem depois de dois pontos: {premium:N2}. A cultura em uso decide o separador decimal e o símbolo de moeda. Em pt-PT, 1234.5 com N2 dá 1 234,50. Em servidores configurados com outra cultura o resultado muda, por isso em APIs convém fixar a cultura.",
 pit="Formatar valores para o utilizador e para ficheiros/JSON com a mesma cultura. Dados máquina-a-máquina devem usar CultureInfo.InvariantCulture."),
"m1:18": dict(
 more="Um método tem assinatura (nome, parâmetros, tipo de retorno) e corpo. Quando o corpo é uma só expressão, => abrevia. Os parâmetros podem ter valor por omissão e podem ser passados pelo nome, o que deixa chamadas com vários bool muito mais legíveis.",
 tryit="Cria CalculatePremium(decimal basePremium, decimal discount = 0m) e chama-o com e sem desconto, com o parâmetro nomeado."),
# ---------------- C# · Objetos ----------------
"m1:21": dict(
 more="Uma class representa algo com identidade: duas apólices com os mesmos dados continuam a ser dois objetos. Um record representa dados: dois records com os mesmos valores são iguais, e o ToString já mostra as propriedades.\n\nUsa record para valores e DTOs; usa class para entidades com comportamento e estado que muda.",
 tryit="Cria o mesmo tipo como class e como record, instancia dois objetos iguais e compara-os com ==."),
"m1:22": dict(
 more="Propriedades são a forma de expor estado. get lê, set escreve, init só deixa escrever na criação do objeto. private set é a escolha para estado que só a própria classe pode alterar, com validação.\n\nAssim, o objeto garante que nunca fica num estado inválido: quem o usa não consegue pôr um prémio negativo.",
 pit="Propriedades públicas com set para tudo. A classe perde o controlo sobre as suas próprias regras."),
"m1:23": dict(
 more="Uma interface é um contrato. IPremiumCalculator diz que existe um método Calculate, mas não como. BasicPremium e DiscountedPremium cumprem o contrato de formas diferentes, e quem usa a interface não precisa de saber qual recebeu.\n\nÉ esta ideia que mais à frente permite a Dependency Injection e os mocks nos testes.",
 tryit="Implementa duas classes de IPremiumCalculator e escolhe uma por argumento da linha de comandos."),
"m1:24": dict(
 more="Composição significa 'tem um': a classe recebe outro objeto e delega-lhe trabalho. Herança significa 'é um' e fixa a classe à sua base. Em geral compõe-se, e herda-se só quando a relação 'é um' é verdadeira em qualquer situação.\n\nTrocar o objeto recebido muda o comportamento sem tocar na classe, e é exatamente isso que a Dependency Injection automatiza."),
"m1:25": dict(
 more="List<T> mantém ordem e permite aceder por índice. Dictionary<K,V> procura por chave em tempo praticamente constante, ideal para encontrar uma apólice pelo número.\n\nO indexador dict[key] lança KeyNotFoundException se a chave não existir. TryGetValue devolve bool e preenche o valor, sem exceção.",
 pit="Usar List e procurar com um ciclo quando a pesquisa é sempre por chave."),
"m1:26": dict(
 more="Um genérico é código escrito uma vez para vários tipos. List<T> funciona para List<int> e List<Policy> com verificação do compilador. Com where podes exigir que T implemente uma interface ou tenha construtor sem parâmetros.",
 tryit="Escreve um método genérico Largest<T>(List<T> items) where T : IComparable<T>."),
# ---------------- C# · LINQ ----------------
"m1:29": dict(
 more="LINQ consulta qualquer coleção com a mesma linguagem: Where filtra, Select transforma, OrderBy ordena, GroupBy agrupa, Sum/Count/Average agregam.\n\nA execução é diferida: a consulta só corre quando a enumeras (foreach, ToList, Count...). Se a coleção mudar entre a definição e a enumeração, o resultado reflete a mudança.",
 pit="Enumerar a mesma consulta várias vezes. Cada enumeração repete o trabalho; guarda o resultado com ToList quando precisares.",
 tryit="Com uma lista de apólices, calcula o total de prémios por cliente com GroupBy e Sum."),
"m1:30": dict(
 more="ICollection<T> é a interface para coleções que se podem contar e alterar. Se um método aceita ICollection<T> em vez de List<T>, aceita também HashSet<T> e outras. Regra prática: pedir o tipo mais geral que o método realmente precisa."),
"m1:31": dict(
 more="IQueryable<T> não guarda dados: guarda uma descrição da consulta. O provider (por exemplo, o do EF Core) traduz essa descrição para SQL e só vai à base de dados quando a consulta é executada.\n\nPor isso o Where deve vir antes do ToList: o filtro corre na base de dados e não em memória.",
 pit="Chamar ToList cedo e filtrar depois: a tabela inteira é carregada para memória."),
"m1:32": dict(
 more="Uma exceção interrompe o fluxo normal e sobe a pilha de chamadas até encontrar um catch compatível. Apanha do tipo mais específico para o mais genérico. finally corre sempre, com ou sem erro, e serve para libertar recursos.\n\nSó apanhes o que sabes tratar. Um catch (Exception) que engole o erro esconde problemas reais.",
 pit="catch vazio. O programa continua, mas ninguém sabe que algo correu mal."),
"m1:33": dict(
 more="Lança exceções com o tipo certo (ArgumentException, InvalidOperationException) e uma mensagem que diz o que falhou e com que valor. ArgumentNullException.ThrowIfNull valida argumentos em uma linha.\n\nDentro de um catch, throw; preserva a stack trace original. throw ex; reescreve-a e perde a origem do erro. Para entradas inválidas do utilizador, TryParse evita exceções no fluxo normal.",
 pit="throw ex; dentro de um catch."),
"m1:34": dict(
 more="Uma exceção própria dá nome a uma regra de negócio: PolicyNotFoundException diz mais do que InvalidOperationException. Herda de Exception, termina o nome em Exception e acrescenta as propriedades com o contexto (por exemplo, o número da apólice).\n\nMais à frente, na API, é por este tipo que o middleware decide o código HTTP a devolver.",
 tryit="Cria InvalidPolicyException com a propriedade Number e lança-a quando o prémio for negativo."),
"m1:35": dict(
 more="Esperar por rede, disco ou base de dados não gasta CPU, mas uma thread bloqueada continua ocupada. Com await a thread é libertada enquanto a operação decorre e retoma quando termina. Numa API, isto significa servir mais pedidos com o mesmo número de threads.\n\nO código lê-se de cima para baixo, como se fosse síncrono."),
"m1:36": dict(
 more="Um método async devolve Task (sem valor) ou Task<T> (com valor). Por convenção, termina em Async. Chamar o método sem await devolve a Task por terminar, não o resultado.",
 pit="async void. Quem chama não consegue esperar nem apanhar exceções; só se usa em event handlers.",
 tryit="Escreve GetQuoteAsync que espera 200 ms com Task.Delay e devolve 1.04m."),
"m1:37": dict(
 more="Para correr várias operações independentes ao mesmo tempo: arranca todas as tarefas primeiro, guarda as Tasks e só depois faz await Task.WhenAll(...). Se fizeres await logo na primeira, corre tudo em sequência.\n\nParallel.ForEachAsync permite limitar a concorrência, útil quando o serviço do outro lado só aguenta um certo número de pedidos.",
 pit="Fazer await dentro do ciclo e pensar que está em paralelo."),
"m1:38": dict(
 more="Uma exceção dentro de um método async fica guardada na Task e é lançada no await. Por isso o try/catch tem de rodear o await, e não a chamada. Se nunca esperares pela Task, o erro passa despercebido.\n\nCom Task.WhenAll, o await lança a primeira exceção; as restantes ficam disponíveis em task.Exception."),
"m1:39": dict(
 more="O cancelamento é cooperativo: o CancellationToken só avisa. Quem executa tem de o receber e verificar (os métodos do .NET já o fazem e lançam OperationCanceledException). Passa o token a todas as chamadas async encadeadas.\n\nNuma API, o ASP.NET Core dá-te o token do pedido HTTP: se o cliente fechar a ligação, o trabalho é cancelado.",
 tryit="Reduz o tempo do CancellationTokenSource para 100 ms e confirma que o catch corre."),
# ---------------- .NET · Plataforma ----------------
"m2:7": dict(
 more="O compilador Roslyn transforma o teu C# em IL (Intermediate Language), guardado num ficheiro .dll. O IL não é código máquina: é igual em Windows, Linux e macOS. Quando a aplicação arranca, o runtime (CLR) usa o compilador JIT para converter o IL em código máquina do processador onde está a correr.\n\nÉ isto que permite compilar uma vez e executar em vários sistemas, incluindo containers Linux."),
"m2:8": dict(
 more="O SDK é o que instalas no teu computador para desenvolver: compilador, comando dotnet e templates. O runtime é o mínimo necessário para executar uma aplicação já compilada, e é o que o servidor precisa.\n\nAs versões pares (8, 10) são LTS. Em projetos novos escolhe sempre uma LTS ou superior, e nunca o .NET Framework 4.x.",
 tryit="No terminal, corre dotnet --list-sdks e dotnet --list-runtimes e vê o que tens instalado."),
"m2:10": dict(
 more="A solução (.sln) é só uma lista de projetos para o IDE abrir em conjunto. Cada projeto (.csproj) é um XML pequeno que diz o que é (Sdk), para que versão compila (TargetFramework), de que pacotes depende (PackageReference) e de que outros projetos depende (ProjectReference).\n\nAs referências entre projetos formam a arquitetura: se o Domain não referencia nada, é impossível usar o EF Core lá dentro por engano.",
 pit="Referências circulares entre projetos. O compilador recusa: é sinal de que as responsabilidades estão mal divididas."),
# ---------------- .NET · ASP.NET Core ----------------
"m2:13": dict(
 more="O Program.cs tem duas fases. Primeiro o builder regista os serviços de que a aplicação precisa (controllers, OpenAPI, base de dados). Depois, com app = builder.Build(), configuras o pipeline: o que acontece a cada pedido, pela ordem em que escreves.\n\nO servidor web por baixo chama-se Kestrel e arranca com app.Run()."),
"m2:15": dict(
 more="Um middleware é um passo do pipeline. Recebe o contexto do pedido e uma função next. O código antes de await next() corre à ida; o código depois corre à volta, já com a resposta construída.\n\nÉ o sítio certo para preocupações transversais: medir tempos, registar pedidos, converter exceções em respostas HTTP.",
 pit="Registar o middleware de erros depois dos controllers. A ordem do registo é a ordem de execução."),
"m2:16": dict(
 more="A configuração vem de várias fontes sobrepostas: appsettings.json, appsettings.{Environment}.json, variáveis de ambiente. A última a ser lida ganha. Assim o mesmo código usa uma base de dados em DEV e outra em PROD, sem recompilar.\n\nSegredos (passwords, chaves) nunca vão para o repositório; usam-se variáveis de ambiente, user-secrets em desenvolvimento ou um cofre."),
"m2:17": dict(
 more="Um controller é uma classe que agrupa endpoints. [ApiController] ativa o binding automático e a validação; [Route] define o caminho base; cada método tem um atributo de verbo. Parâmetros como {number} vêm da rota, e o corpo JSON é convertido para o tipo do parâmetro."),
"m2:19": dict(
 more="O código de estado é parte do contrato da API. Os métodos auxiliares (Ok, NotFound, BadRequest, CreatedAtAction) devolvem o código certo. ActionResult<T> permite devolver tanto o objeto como um código de erro, e o OpenAPI percebe o tipo.",
 tryit="Faz GET de uma apólice que não existe e confirma que recebes 404 e não 200 com corpo vazio."),
"m2:20": dict(
 more="Um DTO descreve o formato do pedido ou da resposta, e não o da tabela. Separar entrada de saída (NewPolicy vs PolicyResponse) permite alterar a base de dados sem partir os clientes da API, e impede que o cliente defina campos que não deve (como o Id).\n\nOs atributos de validação ([Required], [Range], [StringLength]) são verificados antes de o controller correr; com [ApiController], um pedido inválido devolve 400 sozinho.",
 pit="Devolver a entidade da base de dados diretamente. Qualquer alteração à tabela passa a alterar o contrato público."),
"m2:22": dict(
 more="OpenAPI é um documento (JSON) que descreve a API: endpoints, parâmetros, respostas. É gerado a partir do código. O Swagger UI lê esse documento e dá-te uma página para experimentar cada endpoint no browser. Postman e Bruno importam o mesmo documento para criar coleções de pedidos.",
 tryit="Abre /openapi/v1.json e depois a UI, executa um POST e vê o 201 com o cabeçalho Location."),
# ---------------- .NET · DI ----------------
"m2:27": dict(
 more="O container de DI é uma fábrica configurável. No Program.cs dizes 'quando alguém pedir IPremiumCalculator, entrega DiscountedPremium'. O ASP.NET Core cria o controller por cada pedido, olha para o construtor e resolve cada parâmetro recursivamente.\n\nTrocar de implementação é mudar uma linha de registo. O resto do código não se altera.",
 pit="Registar a classe mas esquecer-se de registar uma das suas dependências. O erro surge em execução, no primeiro pedido."),
"m2:28": dict(
 more="Transient cria uma instância nova de cada vez. Scoped cria uma por pedido HTTP, e é o tempo de vida do DbContext. Singleton cria uma para toda a aplicação.\n\nUm Singleton nunca deve receber um Scoped no construtor: viveria mais do que a sua dependência, que já teria sido descartada.",
 pit="Singleton que depende do DbContext. Dá erro de validação do container, ou pior, partilha um DbContext entre pedidos."),
"m2:29": dict(
 more="ILogger<T> regista mensagens com nível (Information, Warning, Error) e categoria (o tipo T). Usa marcadores nomeados, como {Number}, em vez de concatenar: o texto fica constante e os valores ficam pesquisáveis nos sistemas de logs.\n\nIOptions<T> liga uma secção do appsettings a uma classe tipada."),
# ---------------- .NET · EF Core ----------------
"m2:35": dict(
 more="As entidades são classes simples. Por convenção, uma propriedade chamada Id (ou ClassNameId) é a chave primária. CustomerId é a chave estrangeira para Customer, e as propriedades de navegação (Customer, Policies) permitem percorrer a relação em C# sem escrever JOINs."),
"m2:36": dict(
 more="São precisos três elementos: o pacote do provider (Microsoft.EntityFrameworkCore.SqlServer), o pacote Design (para gerar migrations) e a ferramenta global dotnet-ef. A connection string fica no appsettings, e não no código.",
 pit="Instalar o pacote Design só no projeto errado. Os comandos dotnet ef precisam de o encontrar no projeto de arranque."),
"m2:37": dict(
 more="O DbContext representa uma sessão com a base de dados. Cada DbSet<T> é uma tabela. É registado no container com AddDbContext, que o torna Scoped, e recebe as opções (provider e connection string) no construtor."),
"m2:38": dict(
 more="As convenções cobrem o caso simples. Para o resto usa a Fluent API no OnModelCreating: tamanhos máximos, índices únicos (por exemplo, no número da apólice), precisão de decimais e relações. Fica no DbContext, e as entidades continuam livres de detalhes de base de dados.",
 pit="Esquecer a precisão do decimal. O EF avisa, e o valor pode ser truncado na base de dados."),
"m2:39": dict(
 more="dotnet ef migrations add compara o modelo atual com o snapshot da última migration e gera um ficheiro C# com os métodos Up (aplicar) e Down (desfazer). Lê sempre o ficheiro gerado antes de o aplicar: é aí que vês, por exemplo, uma coluna que ia ser apagada."),
"m2:40": dict(
 more="dotnet ef database update cria a base de dados, se não existir, e aplica as migrations pendentes. A tabela __EFMigrationsHistory regista o que já foi aplicado, por isso podes correr o comando várias vezes. Em produção não se aplica diretamente: gera-se um script SQL, revê-se e executa-se com o processo normal de Release.",
 tryit="Acrescenta uma propriedade a Policy, cria uma nova migration e abre o ficheiro gerado."),
"m2:41": dict(
 more="Consultar com o EF é usar o LINQ que já conheces sobre um DbSet. Include carrega a relação na mesma consulta (um JOIN). Os métodos Async (ToListAsync, FirstOrDefaultAsync) libertam a thread. AsNoTracking diz ao EF que não vais alterar os resultados, o que torna a consulta mais leve."),
"m2:42": dict(
 more="O EF acompanha as entidades que carrega (change tracking). Alteras uma propriedade, chamas SaveChangesAsync, e o EF gera o UPDATE só dos campos alterados, tudo numa transação. Para inserir, Add + SaveChangesAsync.",
 pit="Esquecer o SaveChangesAsync. Não há erro e nada fica gravado."),
# ---------------- .NET · Testes ----------------
"m2:47": dict(
 more="Um teste unitário segue três passos: Arrange (preparar), Act (executar), Assert (verificar). [Fact] marca o método como teste. Um bom teste lê-se como uma frase: dado este contexto, quando fizer isto, então acontece aquilo."),
"m2:48": dict(
 more="[Theory] corre o mesmo teste com vários dados fornecidos por [InlineData]. Cada caso aparece como teste separado no relatório. É a ferramenta certa para valores-limite: 0, 1, o máximo, o valor negativo."),
"m2:49": dict(
 more="Assert.Equal, True, False, Null, Contains, Single... cada um verifica uma coisa. Assert.Throws<T> confirma que um código lança a exceção certa; para métodos async usa Assert.ThrowsAsync<T> com await."),
"m2:50": dict(
 more="Um mock substitui uma dependência por um objeto falso que controlas: defines o que devolve e depois verificas como foi chamado. Com NSubstitute, Substitute.For<IPolicyRepository>() cria o falso. Só funciona porque a dependência é uma interface, e é por isso que a Dependency Injection e os testes andam juntos."),
# ---------------- .NET · Organização ----------------
"m2:56": dict(
 more="Cada camada é um projeto. As referências entre projetos impõem a regra: Domain não referencia nada; Application referencia Domain; Infrastructure referencia Application; Api referencia Application e Infrastructure (só para registar). Se alguém tentar usar o EF Core no Domain, o código não compila."),
"m2:57": dict(
 more="O repositório é um contrato definido na Application (IPolicyRepository) e implementado na Infrastructure com o EF Core. Os handlers só conhecem a interface. Para trocar de base de dados escreves outra implementação e mudas o registo no container."),
"m2:59": dict(
 more="O comando é um objeto só com dados (por exemplo, um record CreatePolicyCommand). O handler tem um método HandleAsync com a lógica do caso de uso. O controller só converte o DTO em comando e chama o handler. Como o handler depende de interfaces, testa-se sozinho com mocks.",
 tryit="Escreve um teste ao CreatePolicyHandler com um IPolicyRepository falso que diz que o número já existe."),
}

QUIZ = {
"csharp-1": [
 dict(q="Que tipo deves usar para guardar um prémio de seguro?", o=["double", "decimal", "float", "int"], a=1, w="decimal trabalha em base 10 e não tem os erros de arredondamento de double ou float."),
 dict(q="O que devolve 7 / 2 quando os dois valores são int?", o=["3.5", "4", "3", "Lança uma exceção"], a=2, w="A divisão entre inteiros é inteira. Para 3.5 um dos operandos tem de ser decimal ou double."),
 dict(q="O que faz email ?? \"n/a\" quando email é null?", o=["Lança NullReferenceException", "Devolve \"n/a\"", "Devolve null", "Não compila"], a=1, w="?? devolve o valor da direita quando o da esquerda é null."),
 dict(q="Qual o ciclo que corre pelo menos uma vez?", o=["for", "foreach", "while", "do-while"], a=3, w="do-while testa a condição no fim de cada volta."),
],
"csharp-2": [
 dict(q="Qual a principal diferença entre record e class?", o=["O record não pode ter métodos", "O record compara por valor", "A class é mais rápida", "O record é sempre mutável"], a=1, w="Dois records com os mesmos valores são iguais. Duas instâncias de class só são iguais se forem o mesmo objeto."),
 dict(q="O que permite uma propriedade com init?", o=["Escrever em qualquer momento", "Escrever só ao criar o objeto", "Só ler", "Escrever apenas dentro da classe"], a=1, w="init só aceita atribuição na criação do objeto."),
 dict(q="Porque é que TryGetValue é preferível ao indexador de um Dictionary?", o=["É mais curto", "Não lança exceção se a chave não existir", "Ordena os valores", "Evita duplicados"], a=1, w="O indexador lança KeyNotFoundException; TryGetValue devolve false."),
],
"csharp-3": [
 dict(q="Quando é que uma consulta LINQ é efetivamente executada?", o=["Quando é definida", "Quando é enumerada (ToList, foreach, Count...)", "Quando o programa arranca", "Nunca, é só uma descrição"], a=1, w="Execução diferida: a consulta corre quando enumeras."),
 dict(q="Qual a diferença entre throw; e throw ex; dentro de um catch?", o=["Nenhuma", "throw; preserva a stack trace original", "throw ex; é mais rápido", "throw; só funciona em async"], a=1, w="throw ex; reescreve a stack trace e perdes o ponto onde o erro nasceu."),
 dict(q="Como corres três chamadas async independentes ao mesmo tempo?", o=["await em cada uma, uma a seguir à outra", "Arrancar as Tasks e fazer await Task.WhenAll", "Usar async void", "Usar um ciclo for"], a=1, w="Primeiro arrancas as tarefas, depois esperas por todas."),
 dict(q="O que faz o CancellationToken?", o=["Cancela sozinho qualquer operação", "Avisa quem executa; é este que tem de o verificar", "Apaga a Task", "Torna o método síncrono"], a=1, w="O cancelamento é cooperativo."),
],
"dotnet-1": [
 dict(q="O que contém um ficheiro .dll gerado pelo compilador?", o=["Código máquina para Windows", "IL (Intermediate Language)", "Código C# minificado", "Apenas metadados"], a=1, w="O IL é convertido em código máquina pelo JIT, na altura de executar."),
 dict(q="Qual a diferença entre SDK e runtime?", o=["Nenhuma", "O SDK serve para desenvolver; o runtime para executar", "O runtime inclui o compilador", "O SDK só existe no Windows"], a=1, w="Num servidor basta o runtime; no teu computador instalas o SDK."),
 dict(q="Que elemento do .csproj liga um projeto a outro?", o=["PackageReference", "ProjectReference", "TargetFramework", "ImplicitUsings"], a=1, w="PackageReference traz pacotes NuGet; ProjectReference liga projetos."),
],
"dotnet-2": [
 dict(q="Que código HTTP devolve um POST que criou uma apólice?", o=["200 OK", "201 Created", "204 No Content", "202 Accepted"], a=1, w="201 Created, com o cabeçalho Location do novo recurso."),
 dict(q="O que acontece à ordem dos middlewares no Program.cs?", o=["É irrelevante", "É a ordem de execução do pipeline", "Corre ao contrário", "O framework reordena-os"], a=1, w="Cada middleware corre pela ordem do registo; a resposta volta em sentido contrário."),
 dict(q="Porque se usam DTOs em vez de devolver a entidade?", o=["Por exigência do EF Core", "Para separar o contrato da API do modelo da base de dados", "Para o JSON ficar mais pequeno", "Porque as entidades não são serializáveis"], a=1, w="Assim a base de dados pode mudar sem partir os clientes da API."),
 dict(q="Qual o código para uma apólice com número repetido?", o=["400", "404", "409", "500"], a=2, w="409 Conflict: o pedido conflita com o estado atual."),
],
"dotnet-3": [
 dict(q="Qual o tempo de vida do DbContext por omissão?", o=["Transient", "Scoped", "Singleton", "Static"], a=1, w="AddDbContext regista-o como Scoped: uma instância por pedido HTTP."),
 dict(q="Porque é problemático um Singleton depender de um Scoped?", o=["Não compila", "O Singleton vive mais e fica com um objeto já descartado", "É mais lento", "O container recusa Singletons"], a=1, w="O Singleton vive durante toda a aplicação e o Scoped só durante o pedido."),
 dict(q="Onde se escolhe a implementação de IPremiumCalculator?", o=["No construtor do controller", "No registo do container, no Program.cs", "Na própria interface", "No appsettings"], a=1, w="O registo decide; a classe só declara o que precisa."),
],
"dotnet-4": [
 dict(q="Em code-first, qual é a fonte de verdade do esquema?", o=["A base de dados", "As classes C# e as migrations", "O SQL escrito à mão", "O Swagger"], a=1, w="Escreves o modelo e o EF gera o esquema."),
 dict(q="Porque é perigoso chamar ToList antes do Where num DbSet?", o=["Não compila", "Traz a tabela toda para memória", "Apaga linhas", "Desativa o tracking"], a=1, w="O filtro passa a correr em memória e não na base de dados."),
 dict(q="Alteraste uma propriedade de uma entidade carregada. Que falta para gravar?", o=["Chamar Update()", "Chamar SaveChangesAsync()", "Nada, grava sozinho", "Criar uma migration"], a=1, w="O EF deteta a alteração, mas só grava em SaveChangesAsync."),
 dict(q="O que regista a tabela __EFMigrationsHistory?", o=["Os erros do EF", "As migrations já aplicadas", "Os dados apagados", "As connection strings"], a=1, w="É assim que o EF sabe o que ainda falta aplicar."),
],
"dotnet-5": [
 dict(q="O que representa o 'Arrange' num teste?", o=["Executar o código", "Preparar os objetos e os dados", "Verificar o resultado", "Limpar a base de dados"], a=1, w="Arrange, Act, Assert: preparar, executar, verificar."),
 dict(q="Quando usar [Theory] em vez de [Fact]?", o=["Quando o teste é lento", "Quando o mesmo teste corre com vários dados", "Quando há exceções", "Quando há mocks"], a=1, w="[InlineData] fornece cada caso e cada um aparece como teste separado."),
 dict(q="Porque é que um mock exige que a dependência seja uma interface?", o=["Por regra do xUnit", "Porque é preciso poder substituí-la por um falso", "Porque o EF o exige", "Não exige"], a=1, w="Sem interface (ou método virtual), não há como substituir a implementação."),
],
"dotnet-6": [
 dict(q="Que projeto não referencia nenhum outro numa Clean Architecture?", o=["Api", "Infrastructure", "Application", "Domain"], a=3, w="As dependências apontam para dentro, e o Domain está no centro."),
 dict(q="Onde fica a interface IPolicyRepository e onde a sua implementação?", o=["Ambas no Domain", "Interface na Application, implementação na Infrastructure", "Ambas na Api", "Interface na Infrastructure, implementação na Application"], a=1, w="Quem usa o contrato define-o; quem fala com o EF Core implementa-o."),
 dict(q="Qual a regra simples do CQRS?", o=["Tudo é um comando", "Se altera o estado é comando; se só lê é consulta", "Comandos são sempre assíncronos", "Consultas usam sempre cache"], a=1, w="Comandos pedem alterações; consultas só leem."),
 dict(q="Qual o papel do controller no percurso de um pedido?", o=["Aplicar as regras de negócio", "Converter HTTP em comandos e consultas", "Gerar SQL", "Guardar dados"], a=1, w="O handler decide, o repositório guarda e o controller traduz HTTP."),
],
}

# One-line intro for each chapter
INTRO = {
"csharp-1": "As peças básicas da linguagem: tipos, operadores, decisões, repetições, texto e métodos.",
"csharp-2": "Como representar o domínio de uma seguradora com classes, records, interfaces e coleções.",
"csharp-3": "Consultar coleções com LINQ, tratar erros e esperar por operações lentas sem bloquear.",
"csharp-4": "O enunciado de uma aplicação de consola completa, para juntar tudo o que aprendeste.",
"dotnet-1": "O que acontece entre escrever C# e ver o programa a correr, e como se organiza uma solução.",
"dotnet-2": "Construir uma Web API: pipeline, controllers, códigos HTTP, DTOs, validação e documentação.",
"dotnet-3": "Deixar o container criar e entregar as dependências em vez de fazer new.",
"dotnet-4": "Ligar a API a uma base de dados com classes C#, migrations e consultas LINQ.",
"dotnet-5": "Provar que o código funciona com testes rápidos e isolados.",
"dotnet-6": "Separar responsabilidades em camadas para o código poder crescer sem se complicar.",
}
