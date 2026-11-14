---
title: "Fundamentos da linguagem"
description: "As peças básicas da linguagem: tipos, operadores, decisões, repetições, texto e métodos."
sidebar:
  order: 1
---

As peças básicas da linguagem: tipos, operadores, decisões, repetições, texto e métodos.

## Tipos e variáveis

```csharp
int age = 42;
decimal balance = 320.50m;   // money: decimal
bool active = true;
string name = "Ana Pereira";
var total = balance * 1.04m; // inferred type: decimal
```

- Valor ou referência: int, decimal e bool são valores; string e classes são referências.
- Dinheiro é decimal, nunca double.
- var deixa o compilador inferir o tipo.

<details>
<summary>Saber mais</summary>

Em C# cada variável tem um tipo fixo, decidido em compilação. Os tipos de valor (int, decimal, bool) guardam o próprio valor; os de referência (string, classes) guardam um apontador para o objeto. Na prática, isto muda o que acontece quando copias uma variável ou a passas a um método.

Os tipos double e float guardam números em binário e não conseguem representar 0.1 exatamente. O decimal trabalha em base 10, por isso é o tipo certo para dinheiro. O sufixo m em 320.50m diz ao compilador que o literal é decimal.

:::caution[Armadilha]
0.1 + 0.2 == 0.3 devolve false com double. Num banco, esse erro de arredondamento aparece em saldos, juros e comissões.
:::

:::tip[Experimenta]
Antes de correres o código, escreve o tipo que esperas para total. Depois passa o rato por cima de var no IDE e confirma.
:::

</details>

## Operadores: aritméticos, comparação e lógicos

```csharp
int a = 7, b = 2;
Console.WriteLine(a / b);          // 3 (integer division)
Console.WriteLine(a % b);          // 1 (remainder)
Console.WriteLine(a / (decimal)b); // 3.5

bool vip = a > 5 && b != 0;   // AND
bool any = a < 0 || b < 0;  // OR
bool inverse = !vip;          // NOT
a += 3; a++;                  // a becomes 11
```

- / entre inteiros dá um inteiro.
- % devolve o resto.
- \&\& e \|\| param quando o resultado já é certo.
- += e ++ abreviam atribuições.

<details>
<summary>Saber mais</summary>

A divisão entre dois inteiros é inteira: 7 / 2 dá 3. Para obter 3.5, pelo menos um dos operandos tem de ser decimal ou double. O operador % devolve o resto e é útil para testar múltiplos (é a base do FizzBuzz).

Os operadores \&\& e \|\| são de curto-circuito: se o lado esquerdo já decide o resultado, o direito nem é avaliado. Isso permite escrever user != null \&\& user.IsActive sem rebentar.

:::caution[Armadilha]
Dividir inteiros e esperar um decimal. Converter o resultado depois da divisão já é tarde demais.
:::

:::tip[Experimenta]
Calcula 7 / 2, 7 % 2 e 7m / 2 e compara os três resultados.
:::

</details>

## Operadores de null: ?, ?. , ?? e ??=

```csharp
string? email = null;      // ? = nullable
int? age = null;

int n = email?.Length ?? 0;   // ?. e ??
email ??= "no e-mail";       // assigns only if null
Console.WriteLine(email);     // no e-mail

int years = age ?? 0;       // default value
```

- T? aceita null (string?, int?).
- ?. para se o valor for null.
- ?? atribui um valor por omissão.
- ??= atribui só se for null.

<details>
<summary>Saber mais</summary>

Desde o C# 8, o compilador distingue string (nunca null) de string? (pode ser null) quando o projeto tem Nullable ativo. Os operadores de null existem para lidar com isto sem encher o código de ifs.

?. devolve null em vez de lançar NullReferenceException. ?? dá um valor alternativo. ??= atribui só quando a variável ainda é null, o que é prático para valores por omissão.

:::caution[Armadilha]
Usar ! (null-forgiving) para calar um aviso. O aviso estava a proteger-te de um erro em execução.
:::

:::tip[Experimenta]
Declara string? email = null; e escreve email?.ToUpper() ?? "n/a". Troca o valor para "a@b.pt" e vê a diferença.
:::

</details>

## Operadores: ternário, is e nameof

```csharp
int years = 12;
string kind = years >= 10 ? "loyal" : "new";   // ternary

object value = "AC-001";
if (value is string s && s.StartsWith("AP"))
    Console.WriteLine(s);                  // is + variable

bool ok = years is >= 5 and < 20;         // range
string name = nameof(years);              // "years"
```

- c ? a : b escolhe entre dois valores.
- is testa o tipo e declara a variável.
- and, or, not combinam padrões.
- nameof evita nomes escritos à mão.

<details>
<summary>Saber mais</summary>

O operador ternário c ? a : b é uma expressão: devolve um valor, por isso pode ser usado dentro de uma atribuição ou de uma interpolação. Se a condição precisa de mais de duas ramificações, um switch expression fica mais legível.

O operador is faz pattern matching: testa o tipo e, no mesmo passo, declara uma variável já convertida (obj is Account p). Os padrões and, or e not permitem escrever intervalos como age is \>= 18 and \< 65.

:::caution[Armadilha]
Encadear ternários dentro de ternários. Passados dois níveis, troca por um switch expression.
:::

:::tip[Experimenta]
Escreve um método que recebe object e devolve texto diferente para int, string e Account usando is.
:::

</details>

## Condições: if e else

```csharp
static string Classify(decimal balance)
{
    if (balance >= 1000m)
        return "high";
    else if (balance >= 300m)
        return "medium";
    else
        return "low";
}
```

- if avalia uma condição bool.
- else if só é testado se a anterior falhar.
- Usar chavetas quando o bloco tem várias linhas.
- Retornar cedo evita ifs aninhados.

<details>
<summary>Saber mais</summary>

O if avalia sempre um bool. Em C# não existe a conversão implícita de números ou objetos para bool, o que evita erros do tipo if (x = 5).

A técnica de retornar cedo (guard clauses) trata primeiro os casos inválidos e sai do método. O caminho feliz fica no fim, sem aninhamento.

:::caution[Armadilha]
Omitir as chavetas num bloco de várias linhas. Só a primeira linha pertence ao if.
:::

:::tip[Experimenta]
Reescreve um if/else aninhado com três níveis usando retornos antecipados.
:::

</details>

## Condições: switch

```csharp
static string Season(int month)
{
    switch (month)
    {
        case 12:
        case 1:
        case 2:
            return "winter";
        case 6 or 7 or 8:
            return "summer";
        default:
            return "other season";
    }
}
```

- case seguidos partilham o resultado.
- default apanha o resto.
- Cada case termina com return ou break.
- or agrupa valores.

<details>
<summary>Saber mais</summary>

O switch clássico compara uma variável com vários valores. Cada case tem de terminar com break ou return; o C# não permite o 'fall through' acidental de outras linguagens. Cases seguidos sem código partilham o mesmo resultado.

:::caution[Armadilha]
Esquecer o default. Se aparecer um valor inesperado, o programa segue em frente sem fazer nada.
:::

:::tip[Experimenta]
Mapeia o código de um estado (1, 2, 3) para o texto 'Ativa', 'Cancelada', 'Suspensa' e testa com um valor fora do intervalo.
:::

</details>

## Condições: switch inline (expressão)

```csharp
static string Season(int month) => month switch
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
};
```

- switch como expressão devolve um valor.
- =\> liga cada padrão ao resultado.
- \_ é o caso por omissão.
- Aceita intervalos e combinações.

<details>
<summary>Saber mais</summary>

O switch expression devolve um valor e usa =\> em vez de case/break. Cada braço é um padrão, o que permite relacionais (\< 18), combinações (and/or) e propriedades. O \_ funciona como default. Se nenhum braço cobrir o valor, o compilador avisa.

:::tip[Experimenta]
Escreve um switch expression que devolve o bónus da taxa de juro (0, 0.5%, 1%) consoante os anos de cliente, com intervalos.
:::

</details>

## Ciclos: foreach e for

```csharp
var names = new List<string> { "Ana", "Rui", "Inês" };

foreach (var name in names)
    Console.WriteLine(name);

for (int i = 0; i < names.Count; i++)
    Console.WriteLine($"{i + 1}. {names[i]}");

for (int i = 10; i > 0; i -= 3)
    Console.Write(i + " ");   // 10 7 4 1
```

- foreach percorre uma coleção, sem índice.
- for dá controlo do índice e do passo.
- Não alterar a coleção dentro de um foreach.

<details>
<summary>Saber mais</summary>

foreach percorre qualquer coleção sem expor índices, o que elimina erros de 'um a mais' ou 'um a menos'. O for é a ferramenta quando precisas do índice ou de um passo diferente de 1.

Alterar a coleção durante um foreach lança InvalidOperationException. Se precisas de remover elementos, constrói uma nova lista ou usa RemoveAll.

:::caution[Armadilha]
Remover elementos de uma List dentro de um foreach sobre a própria List.
:::

</details>

## Ciclos: while, do-while, break e continue

```csharp
int attempts = 0;
while (attempts < 5)
{
    attempts++;
    if (attempts == 2) continue;   // next round
    if (attempts == 4) break;      // exits the loop
    Console.WriteLine(attempts);
}

string? line;
do
{
    line = Console.ReadLine();
} while (string.IsNullOrWhiteSpace(line));
```

- while testa antes de cada volta.
- do-while corre pelo menos uma vez.
- break sai do ciclo.
- continue passa à volta seguinte.

<details>
<summary>Saber mais</summary>

while testa a condição antes de cada volta, por isso pode não correr nenhuma vez. do-while testa no fim e corre pelo menos uma: é a escolha natural para menus e para pedir um valor até ser válido.

break sai do ciclo; continue salta para a volta seguinte.

:::caution[Armadilha]
Ciclos infinitos por esquecer de atualizar a variável da condição.
:::

:::tip[Experimenta]
Escreve um menu em do-while que só termina quando o utilizador escolhe 0.
:::

</details>

## Strings: construção

```csharp
string a = "Ana";
string b = "Pereira";

string c1 = a + " " + b;                  // concatenation
string c2 = string.Concat(a, " ", b);
string c3 = string.Join(", ", new[] { a, b });

var sb = new StringBuilder();            // many joins
for (int i = 0; i < 3; i++) sb.Append(i).Append(";");
string c4 = sb.ToString();               // "0;1;2;"
```

- \+ serve para poucas junções.
- string.Join une uma coleção com um separador.
- StringBuilder em ciclos longos.
- Uma string nunca muda: cada operação cria outra.

<details>
<summary>Saber mais</summary>

As strings em .NET são imutáveis: cada + cria uma string nova. Para três ou quatro junções não faz diferença. Num ciclo com milhares de iterações, o StringBuilder evita criar milhares de strings intermédias.

string.Join junta uma coleção com um separador sem teres de tratar o último elemento à parte.

:::tip[Experimenta]
Junta os números de 1 a 5 com string.Join(", ", ...).
:::

</details>

## Strings: interpolação

```csharp
var name = "Ana";
decimal balance = 320.5m;

string s1 = $"Hello, {name}!";
string s2 = $"With interest: {balance * 1.02m}";
string s3 = $"{name.ToUpper()} has {name.Length} letters";
string s4 = $"Level: {(balance > 300m ? "alto" : "baixo")}";

string json = $$"""{ "name": "{{name}}" }""";
```

- $"..." insere expressões entre chavetas.
- Aceita operadores e chamadas de métodos.
- Condições vão entre parênteses.
- """ evita escapar aspas.

<details>
<summary>Saber mais</summary>

A interpolação $"..." é a forma preferida de construir texto. Dentro das chavetas podes usar qualquer expressão, incluindo chamadas de métodos e ternários (entre parênteses). As raw strings com três aspas dispensam escapes e são ideais para JSON e SQL de teste.

:::caution[Armadilha]
Esquecer o $ no início e ver as chavetas escritas literalmente no ecrã.
:::

</details>

## Strings: formatação

```csharp
decimal p = 1234.5m;
var d = new DateTime(2026, 10, 21);

$"{p:N2}"            // 1,234.50
$"{p:C}"             // $1,234.50
$"{0.15m:P0}"        // 15%
$"{d:dd/MM/yyyy}"    // 21/10/2026
$"{42:D5}"           // 00042
$"{7,5}|{7,-5}|"     // "    7|7    |"
string.Format("{0:N2}", p)   // old way
```

- N2 duas casas; C moeda.
- P0 percentagem; D5 cinco dígitos.
- dd/MM/yyyy formata datas.
- A cultura define separadores e símbolo.

<details>
<summary>Saber mais</summary>

Dentro da interpolação, o formato vem depois de dois pontos: \{balance:N2\}. A cultura em uso decide o separador decimal e o símbolo de moeda. Em pt-PT, 1234.5 com N2 dá 1 234,50. Em servidores configurados com outra cultura o resultado muda, por isso em APIs convém fixar a cultura.

:::caution[Armadilha]
Formatar valores para o utilizador e para ficheiros/JSON com a mesma cultura. Dados máquina-a-máquina devem usar CultureInfo.InvariantCulture.
:::

</details>

## Métodos

```csharp
static decimal CalculateBonus(int customerYears)
{
    if (customerYears >= 10) return 0.015m;
    if (customerYears >= 5) return 0.010m;
    return 0m;
}

static int Add(int a, int b = 0) => a + b;

var b = CalculateBonus(6);   // 0.010
```

- Um método tem nome, parâmetros e tipo de retorno.
- =\> abrevia métodos de uma expressão.
- Parâmetros podem ter valor por omissão.

<details>
<summary>Saber mais</summary>

Um método tem assinatura (nome, parâmetros, tipo de retorno) e corpo. Quando o corpo é uma só expressão, =\> abrevia. Os parâmetros podem ter valor por omissão e podem ser passados pelo nome, o que deixa chamadas com vários bool muito mais legíveis.

:::tip[Experimenta]
Cria CalculateInterest(decimal balance, decimal bonus = 0m) e chama-o com e sem bónus, com o parâmetro nomeado.
:::

</details>

## Cinco exercícios: tipos e fluxo

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **FizzBuzz.** Escreve os números de 1 a 15, trocando-os por «Fizz» se forem múltiplos de 3, por «Buzz» se forem de 5 e por «FizzBuzz» se forem de ambos.
2. **Palíndromo.** Diz se uma palavra se lê da mesma forma de trás para a frente («arara» é palíndromo, «casa» não).
3. **Contar palavras.** Conta quantas palavras tem uma frase escrita pelo utilizador.
4. **Juros com bónus.** Calcula os juros anuais de uma conta, aplicando um bónus à taxa que depende dos anos de cliente.
5. **Validar NIF.** Verifica se um texto é um NIF válido, ou seja, se tem exatamente 9 dígitos numéricos.

:::tip[Dica]
Resolve o FizzBuzz primeiro. Os outros quatro podes fazê-los pela ordem que quiseres.
:::

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

Que tipo deves usar para guardar um saldo bancário?

- **A.** double
- **B.** decimal
- **C.** float
- **D.** int

<details>
<summary>Ver resposta</summary>

**B. decimal**

decimal trabalha em base 10 e não tem os erros de arredondamento de double ou float.

</details>

### Pergunta 2

O que devolve 7 / 2 quando os dois valores são int?

- **A.** 3.5
- **B.** 4
- **C.** 3
- **D.** Lança uma exceção

<details>
<summary>Ver resposta</summary>

**C. 3**

A divisão entre inteiros é inteira. Para 3.5 um dos operandos tem de ser decimal ou double.

</details>

### Pergunta 3

O que faz email ?? "n/a" quando email é null?

- **A.** Lança NullReferenceException
- **B.** Devolve "n/a"
- **C.** Devolve null
- **D.** Não compila

<details>
<summary>Ver resposta</summary>

**B. Devolve "n/a"**

?? devolve o valor da direita quando o da esquerda é null.

</details>

### Pergunta 4

Qual o ciclo que corre pelo menos uma vez?

- **A.** for
- **B.** foreach
- **C.** while
- **D.** do-while

<details>
<summary>Ver resposta</summary>

**D. do-while**

do-while testa a condição no fim de cada volta.

</details>
