---
title: "LINQ, exceções e async/await"
description: "Consultar coleções com LINQ, tratar erros e esperar por operações lentas sem bloquear."
sidebar:
  order: 3
---

Consultar coleções com LINQ, tratar erros e esperar por operações lentas sem bloquear.

## LINQ: consultar dados

```csharp
var sortedAccounts = accounts
    .Where(a => a.Balance > 300m)
    .OrderByDescending(a => a.Balance)
    .Select(a => new { a.Number, a.Balance })
    .ToList();

var totals = accounts
    .GroupBy(a => a.AccountHolder.Name)
    .Select(g => new
    {
        Customer = g.Key,
        Total = g.Sum(a => a.Balance)
    });
```

- LINQ serve para iterar/consultar qualquer coleção, sem ciclos manuais.
- Where filtra e Select transforma.
- GroupBy agrupa e Sum soma.
- Execução diferida: corre quando se enumera.

<details>
<summary>Saber mais</summary>

LINQ consulta qualquer coleção com a mesma linguagem: Where filtra, Select transforma, OrderBy ordena, GroupBy agrupa, Sum/Count/Average agregam.

A execução é diferida: a consulta só corre quando a enumeras (foreach, ToList, Count...). Se a coleção mudar entre a definição e a enumeração, o resultado reflete a mudança.

:::caution[Armadilha]
Enumerar a mesma consulta várias vezes. Cada enumeração repete o trabalho; guarda o resultado com ToList quando precisares.
:::

:::tip[Experimenta]
Com uma lista de contas, calcula o total de saldos por cliente com GroupBy e Sum.
:::

</details>

## LINQ: ICollection

```csharp
ICollection<Account> col = new List<Account>();

col.Add(added);                  // adds
col.Remove(old);             // removes
Console.WriteLine(col.Count);   // how many
bool exists = col.Contains(added);
col.Clear();                    // empties

// query the collection with LINQ
var highBalance = col.Where(a => a.Balance > 300m).ToList();
```

- ICollection\<T\> é uma coleção que se pode contar e alterar.
- Tem Count, Add, Remove, Contains e Clear.
- List\<T\> e HashSet\<T\> implementam-na.
- Usar como tipo do parâmetro aceita várias coleções.

<details>
<summary>Saber mais</summary>

ICollection\<T\> é a interface para coleções que se podem contar e alterar. Se um método aceita ICollection\<T\> em vez de List\<T\>, aceita também HashSet\<T\> e outras. Regra prática: pedir o tipo mais geral que o método realmente precisa.

</details>

## LINQ: IQueryable

```csharp
// 1. describes the query (does not run)
IQueryable<Account> q = context.Accounts
    .Where(a => a.Balance > 300m)
    .OrderBy(a => a.Number);

// 2. generates the SQL and runs it
var lista = await q.ToListAsync();

// SELECT * FROM Accounts
// WHERE Balance > 300 ORDER BY Number
```

- IQueryable\<T\> descreve a consulta; o provider traduz para SQL.
- Só executa no .ToList, .First, .Count...
- Filtrar na base de dados evita carregar dados a mais.

<details>
<summary>Saber mais</summary>

IQueryable\<T\> não guarda dados: guarda uma descrição da consulta. O provider (por exemplo, o do EF Core) traduz essa descrição para SQL e só vai à base de dados quando a consulta é executada.

Por isso o Where deve vir antes do ToList: o filtro corre na base de dados e não em memória.

:::caution[Armadilha]
Chamar ToList cedo e filtrar depois: a tabela inteira é carregada para memória.
:::

</details>

## Exceptions: try, catch e finally

```csharp
try
{
    Console.WriteLine(100 / int.Parse(text));
}
catch (FormatException)
{ Console.WriteLine("Not a number"); }
catch (DivideByZeroException)
{ Console.WriteLine("Zero!"); }
catch (Exception ex)
{ Console.WriteLine(ex.Message); }
finally
{ Console.WriteLine("Done"); }   // always runs
```

- try envolve o código que pode falhar.
- catch apanha por tipo, do mais específico para o mais genérico.
- finally corre sempre: serve para libertar recursos.
- Só apanhar o que se sabe tratar.

<details>
<summary>Saber mais</summary>

Uma exceção interrompe o fluxo normal e sobe a pilha de chamadas até encontrar um catch compatível. Apanha do tipo mais específico para o mais genérico. finally corre sempre, com ou sem erro, e serve para libertar recursos.

Só apanhes o que sabes tratar. Um catch (Exception) que engole o erro esconde problemas reais.

:::caution[Armadilha]
catch vazio. O programa continua, mas ninguém sabe que algo correu mal.
:::

</details>

## Exceptions: lançar e propagar

```csharp
static void Register(Account? a, string text)
{
    ArgumentNullException.ThrowIfNull(a);
    if (a.Balance < 0)
        throw new ArgumentException("Balance < 0");

    if (!decimal.TryParse(text, out var p))
        return;      // no exception
}

catch (Exception ex)
{
    Log(ex);
    throw;          // not: throw ex;
}
```

- throw com o tipo certo e uma mensagem útil.
- ThrowIfNull valida argumentos à entrada.
- throw; propaga e mantém o rasto; throw ex; apaga-o.
- TryParse em vez de exceções no fluxo normal.

<details>
<summary>Saber mais</summary>

Lança exceções com o tipo certo (ArgumentException, InvalidOperationException) e uma mensagem que diz o que falhou e com que valor. ArgumentNullException.ThrowIfNull valida argumentos em uma linha.

Dentro de um catch, throw; preserva a stack trace original. throw ex; reescreve-a e perde a origem do erro. Para entradas inválidas do utilizador, TryParse evita exceções no fluxo normal.

:::caution[Armadilha]
throw ex; dentro de um catch.
:::

</details>

## Exceptions: excepções personalizadas

```csharp
public class InvalidAccountException : Exception
{
    public string Number { get; }

    public InvalidAccountException(string num, string msg)
        : base(msg) => Number = num;
}

throw new InvalidAccountException("AC-001", "Balance < 0");

try { /* ... */ }
catch (InvalidAccountException ex)
{
    Console.WriteLine(ex.Number);
}
```

- Herdar de Exception e dar um nome terminado em Exception.
- Acrescentar propriedades com o contexto do erro.
- base(msg) passa o texto à classe base.
- catch do tipo específico, antes do genérico.

<details>
<summary>Saber mais</summary>

Uma exceção própria dá nome a uma regra de negócio: AccountNotFoundException diz mais do que InvalidOperationException. Herda de Exception, termina o nome em Exception e acrescenta as propriedades com o contexto (por exemplo, o número da conta).

Mais à frente, na API, é por este tipo que o middleware decide o código HTTP a devolver.

:::tip[Experimenta]
Cria InvalidAccountException com a propriedade Number e lança-a quando o saldo for negativo.
:::

</details>

## async/await

```csharp
// blocks the thread for 2 seconds
Thread.Sleep(2000);

// frees the thread while waiting
await Task.Delay(2000);

// real example: HTTP call
using var http = new HttpClient();
string json = await http
    .GetStringAsync("https://example.com/quote");
Console.WriteLine(json.Length);
```

- Esperar por rede, disco ou base de dados não deve bloquear a thread.
- await liberta a thread e retoma quando a operação termina.
- O código lê-se como se fosse sequencial.
- Numa API, liberta a thread para outros pedidos.

<details>
<summary>Saber mais</summary>

Esperar por rede, disco ou base de dados não gasta CPU, mas uma thread bloqueada continua ocupada. Com await a thread é libertada enquanto a operação decorre e retoma quando termina. Numa API, isto significa servir mais pedidos com o mesmo número de threads.

O código lê-se de cima para baixo, como se fosse síncrono.

</details>

## async/await: Task e Task\<T\>

```csharp
// no value
static async Task SaveAsync(Account a)
{
    await Task.Delay(100);
}

// with a value
static async Task<decimal> GetBalanceAsync(string code)
{
    await Task.Delay(200);   // simulates an external call
    return 1.04m;
}

decimal c = await GetBalanceAsync("AC-001");
Task<decimal> t = GetBalanceAsync("AC-002");  // only starts
decimal d = await t;                        // waits here
```

- async marca o método; await espera pelo resultado.
- Task (sem valor) e Task\<T\> (com valor).
- Nome termina em Async.
- Evitar async void, exceto em eventos.

<details>
<summary>Saber mais</summary>

Um método async devolve Task (sem valor) ou Task\<T\> (com valor). Por convenção, termina em Async. Chamar o método sem await devolve a Task por terminar, não o resultado.

:::caution[Armadilha]
async void. Quem chama não consegue esperar nem apanhar exceções; só se usa em event handlers.
:::

:::tip[Experimenta]
Escreve GetBalanceAsync que espera 200 ms com Task.Delay e devolve 1.04m.
:::

</details>

## async: executar em paralelo

```csharp
// sequential: takes the sum of the times
var a = await GetBalanceAsync("AC-001");
var b = await GetBalanceAsync("AC-002");

// parallel: takes as long as the slowest
var t1 = GetBalanceAsync("AC-001");
var t2 = GetBalanceAsync("AC-002");

decimal[] prices = await Task.WhenAll(t1, t2);

// a list of codes, at most 3 at a time
await Parallel.ForEachAsync(codes,
    new ParallelOptions { MaxDegreeOfParallelism = 3 },
    async (code, ct) => await GetBalanceAsync(code));
```

- Task.WhenAll espera por várias tarefas ao mesmo tempo.
- Arrancar as tarefas antes de fazer await.
- Parallel.ForEachAsync limita a concorrência.
- Só faz sentido para trabalho independente.

<details>
<summary>Saber mais</summary>

Para correr várias operações independentes ao mesmo tempo: arranca todas as tarefas primeiro, guarda as Tasks e só depois faz await Task.WhenAll(...). Se fizeres await logo na primeira, corre tudo em sequência.

Parallel.ForEachAsync permite limitar a concorrência, útil quando o serviço do outro lado só aguenta um certo número de pedidos.

:::caution[Armadilha]
Fazer await dentro do ciclo e pensar que está em paralelo.
:::

</details>

## async: gestão de erros

```csharp
static async Task<decimal> GetBalanceAsync(string code)
{
    await Task.Delay(200);
    if (string.IsNullOrEmpty(code))
        throw new ArgumentException("Missing code");
    return 1.04m;
}

try
{
    var c = await GetBalanceAsync("");   // error is raised
}
catch (ArgumentException ex)
{ Console.WriteLine(ex.Message); }

var t = GetBalanceAsync("");   // no await: no error
```

- Um erro num método async é lançado no await.
- O try/catch à volta do await trata-o como qualquer exceção.
- Sem await, a exceção fica guardada na Task e passa despercebida.
- Com Task.WhenAll, o await lança a primeira exceção.

<details>
<summary>Saber mais</summary>

Uma exceção dentro de um método async fica guardada na Task e é lançada no await. Por isso o try/catch tem de rodear o await, e não a chamada. Se nunca esperares pela Task, o erro passa despercebido.

Com Task.WhenAll, o await lança a primeira exceção; as restantes ficam disponíveis em task.Exception.

</details>

## async: cancelamento

```csharp
using var cts = new CancellationTokenSource(1000);   // 1 s
// cts.Cancel();   // or cancel manually

try { await GetBalanceAsync("AC-001", cts.Token); }
catch (OperationCanceledException)
{ Console.WriteLine("Cancelled"); }

static async Task<decimal> GetBalanceAsync(
    string code, CancellationToken ct)
{
    await Task.Delay(200, ct);   // throws if cancelled
    ct.ThrowIfCancellationRequested();
    return 1.04m;
}
```

- O token pede o cancelamento e viaja até quem executa.
- O .NET aceita o token e, ao cancelar, lança uma exceção.
- Em ciclos próprios, verificar o token.
- Numa API, o token do pedido HTTP já vem do ASP.NET.

<details>
<summary>Saber mais</summary>

O cancelamento é cooperativo: o CancellationToken só avisa. Quem executa tem de o receber e verificar (os métodos do .NET já o fazem e lançam OperationCanceledException). Passa o token a todas as chamadas async encadeadas.

Numa API, o ASP.NET Core dá-te o token do pedido HTTP: se o cliente fechar a ligação, o trabalho é cancelado.

:::tip[Experimenta]
Reduz o tempo do CancellationTokenSource para 100 ms e confirma que o catch corre.
:::

</details>

## Saldos das contas

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Exceção própria.** BalanceUnavailableException, com o número da conta.
2. **Saldo assíncrono.** GetBalanceAsync demora 200 ms e lança a exceção se o número terminar em 9.
3. **Em paralelo.** Pedir o saldo de todas as contas com Task.WhenAll.
4. **Falhas isoladas.** Uma conta sem resposta não pode deitar abaixo as outras.
5. **LINQ.** Somar os saldos obtidos e listar as contas sem resposta.

<details>
<summary>Ver resultado esperado</summary>

```text
AC-001: 332,28
AC-002: 332,28
AC-009: indisponível

Total: 664,56
Sem resposta: AC-009
```

</details>

:::note[Extra]
Cancelar tudo ao fim de 150 ms com um CancellationToken e mostrar «Cancelado».
:::
