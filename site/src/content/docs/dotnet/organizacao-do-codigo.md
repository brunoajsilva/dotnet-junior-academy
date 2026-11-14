---
title: "Organização do código"
description: "Separar responsabilidades em camadas para o código poder crescer sem se complicar."
sidebar:
  order: 6
---

Separar responsabilidades em camadas para o código poder crescer sem se complicar.

## Porque organizar em camadas

#### O problema

Controllers que validam, calculam e falam com a base de dados são difíceis de testar e de alterar.

#### A ideia

Cada parte tem uma responsabilidade: receber pedidos, aplicar regras, guardar dados.

#### O ganho

Mudar a base de dados ou a API não obriga a reescrever as regras de negócio.

:::note[Nota]
Neste capítulo, a API dos exercícios anteriores é reorganizada em camadas.
:::

<details>
<summary>Saber mais</summary>

Um controller que valida, calcula os juros e fala com a base de dados faz três trabalhos. Para o testar tens de ter base de dados; para trocar a base de dados mexes no controller. Dividir em camadas dá a cada parte um motivo único para mudar.

</details>

## Clean Architecture

- **Infraestrutura e API**: EF Core, HTTP
- **Aplicação**: casos de uso
- **Domínio**: entidades e regras

- As dependências apontam para dentro.
- O Domínio não conhece o EF Core nem o ASP.NET Core.
- As interfaces ficam dentro; as implementações, fora.

<details>
<summary>Saber mais</summary>

Imagina círculos concêntricos. No centro estão as regras do negócio, que mudam pouco. Nas camadas de fora estão os detalhes técnicos (base de dados, HTTP), que mudam mais. Uma camada só pode conhecer as que estão mais para dentro.

O truque que torna isto possível é a inversão de dependência: a Application declara a interface IAccountRepository e a Infrastructure implementa-a. No Módulo 5 constróis exatamente isto.

:::tip[Experimenta]
Pergunta a ti próprio, para cada classe que escreves: em que círculo vive? E o que é que ela precisa de conhecer?
:::

</details>

## Estrutura da solução

```csharp
BankingApp.sln
├─ BankingApp.Domain          entities and rules
├─ BankingApp.Application     use cases
├─ BankingApp.Infrastructure  EF Core
├─ BankingApp.Api             controllers
└─ BankingApp.Tests           tests

Api            -> Application, Infrastructure
Infrastructure -> Application
Application    -> Domain
Domain         -> (nothing)
```

- Um projeto por camada.
- As referências impõem a regra das dependências.
- O Domínio não referencia nada.
- Só a Api conhece a Infrastructure, para a registar.

<details>
<summary>Saber mais</summary>

Cada camada é um projeto. As referências entre projetos impõem a regra: Domain não referencia nada; Application referencia Domain; Infrastructure referencia Application; Api referencia Application e Infrastructure (só para registar). Se alguém tentar usar o EF Core no Domain, o código não compila.

</details>

## O repositório

```csharp
// Application: the contract
public interface IAccountRepository
{
    Task<Account?> GetAsync(string number);
    Task AddAsync(Account account);
}

// Infrastructure: the implementation
public class AccountRepository : IAccountRepository
{
    private readonly BankingAppContext _ctx;
    public AccountRepository(BankingAppContext c)
        => _ctx = c;

    public Task<Account?> GetAsync(string number)
        => _ctx.Accounts.FirstOrDefaultAsync(
            a => a.Number == number);
}
```

- O contrato fica na Aplicação.
- A implementação com EF Core fica na Infrastructure.
- O resto do código só conhece a interface.
- Trocar a base de dados é trocar a implementação.

<details>
<summary>Saber mais</summary>

O repositório é um contrato definido na Application (IAccountRepository) e implementado na Infrastructure com o EF Core. Os handlers só conhecem a interface. Para trocar de base de dados escreves outra implementação e mudas o registo no container.

</details>

## CQRS: comandos e consultas

#### Comando

Pede uma alteração de estado e não devolve dados de negócio. Exemplo: OpenAccount, CloseAccount.

#### Consulta

Lê dados e nunca altera o estado. Exemplo: GetAccount, ListCustomerAccounts.

#### Handler

Uma classe por comando ou consulta, com um só método. Recebe o pedido e devolve o resultado.

:::note[Nota]
Regra simples: se altera o estado, é um comando; se só lê, é uma consulta.
:::

<details>
<summary>Saber mais</summary>

CQRS (Command Query Responsibility Segregation) separa quem altera de quem lê. Aqui aplica-se na forma simples: classes pequenas, uma por caso de uso. Não é preciso nenhuma biblioteca. Se um dia a equipa adotar uma biblioteca de mediação, confirma primeiro a licença.

</details>

## Handlers

```csharp
public record OpenAccountCommand(
    string Number, int CustomerId, decimal Balance);

public class OpenAccountHandler
{
    private readonly IAccountRepository _repo;
    public OpenAccountHandler(IAccountRepository repo)
        => _repo = repo;

    public async Task<string> Handle(OpenAccountCommand c)
    {
        var acc = new Account(
            c.Number, c.CustomerId, c.Balance);
        await _repo.AddAsync(acc);
        return acc.Number;
    }
}
```

- O comando é um objeto só com dados.
- O handler contém a lógica do caso de uso.
- O controller só chama o handler.
- Cada handler é testável sozinho.

<details>
<summary>Saber mais</summary>

O comando é um objeto só com dados (por exemplo, um record OpenAccountCommand). O handler tem um método HandleAsync com a lógica do caso de uso. O controller só converte o DTO em comando e chama o handler. Como o handler depende de interfaces, testa-se sozinho com mocks.

:::tip[Experimenta]
Escreve um teste ao OpenAccountHandler com um IAccountRepository falso que diz que o número já existe.
:::

</details>

## O percurso de um pedido

1. **Pedido** POST /api/accounts
2. **Controller** valida o DTO
3. **Handler** aplica as regras
4. **Repositório** fala com o EF Core
5. **Base de dados** INSERT

:::note[Nota]
O controller converte HTTP em comandos e consultas.

O handler decide; o repositório guarda.

A resposta faz o caminho inverso, com o código HTTP certo.
:::

<details>
<summary>Saber mais</summary>

Segue o pedido de um POST /api/accounts: o controller converte HTTP em comando, o handler decide, o repositório guarda e a resposta faz o caminho inverso. Cada passo tem uma só responsabilidade, por isso podes testar e alterar cada um sem mexer nos outros.

:::tip[Experimenta]
Abre o Módulo 5 e usa o explorador «Percurso de um pedido» para ver este caminho com código real.
:::

</details>

## A API em camadas

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Projetos.** criar Domain, Application e Infrastructure e referenciá-los pela ordem certa
2. **Mover.** as entidades para o Domain e o DbContext para a Infrastructure
3. **Repositório.** IAccountRepository na Application, implementado na Infrastructure
4. **Handlers.** OpenAccount e GetAccount, injetados no controller
5. **Verificar.** que os testes continuam a passar e que o Domain não referencia o EF Core

<details>
<summary>Ver resultado esperado</summary>

```text
Api            -> Application
               Infrastructure
Infrastructure -> Application
Application    -> Domain
Domain         -> (nothing)
```

</details>

:::note[Extra]
Acrescentar a consulta ListCustomerAccounts com o seu handler.
:::

<details>
<summary>Saber mais</summary>

Só passas ao capítulo seguinte quando o resultado esperado aparecer no teu computador. Se algo falhar, lê a mensagem de erro de baixo para cima: a última linha costuma dizer o que correu mal.

:::tip[Experimenta]
Acrescentar a consulta ListCustomerAccounts com o seu handler.
:::

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

Que projeto não referencia nenhum outro numa Clean Architecture?

- **A.** Api
- **B.** Infrastructure
- **C.** Application
- **D.** Domain

<details>
<summary>Ver resposta</summary>

**D. Domain**

As dependências apontam para dentro, e o Domain está no centro.

</details>

### Pergunta 2

Onde fica a interface IAccountRepository e onde a sua implementação?

- **A.** Ambas no Domain
- **B.** Interface na Application, implementação na Infrastructure
- **C.** Ambas na Api
- **D.** Interface na Infrastructure, implementação na Application

<details>
<summary>Ver resposta</summary>

**B. Interface na Application, implementação na Infrastructure**

Quem usa o contrato define-o; quem fala com o EF Core implementa-o.

</details>

### Pergunta 3

Qual a regra simples do CQRS?

- **A.** Tudo é um comando
- **B.** Se altera o estado é comando; se só lê é consulta
- **C.** Comandos são sempre assíncronos
- **D.** Consultas usam sempre cache

<details>
<summary>Ver resposta</summary>

**B. Se altera o estado é comando; se só lê é consulta**

Comandos pedem alterações; consultas só leem.

</details>

### Pergunta 4

Qual o papel do controller no percurso de um pedido?

- **A.** Aplicar as regras de negócio
- **B.** Converter HTTP em comandos e consultas
- **C.** Gerar SQL
- **D.** Guardar dados

<details>
<summary>Ver resposta</summary>

**B. Converter HTTP em comandos e consultas**

O handler decide, o repositório guarda e o controller traduz HTTP.

</details>
