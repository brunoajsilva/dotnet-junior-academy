---
title: "Dependency Injection"
description: "Deixar o container criar e entregar as dependências em vez de fazer new."
sidebar:
  order: 3
---

Deixar o container criar e entregar as dependências em vez de fazer new.

## Porquê injetar dependências?

#### Sem injeção

A classe escolhe e cria a sua dependência: fica presa a ela.

```csharp
public class AccountService
{
    readonly StandardInterest _calc = new();

    public decimal Interest(Account a)
        => _calc.Calculate(a);
}
```

#### Com injeção

A classe recebe-a pelo construtor: quem cria decide qual usar.

```csharp
public class AccountService
{
    readonly IInterestCalculator _calc;

    public AccountService(
        IInterestCalculator calc)
        => _calc = calc;
}
```

<details>
<summary>Saber mais</summary>

À esquerda, AccountService cria StandardInterest com new: está presa a essa classe e não podes testá-la com outra. À direita recebe IInterestCalculator pelo construtor: quem cria o AccountService decide qual usar. É a mesma ideia da composição que viste em C#.

:::tip[Experimenta]
Cria um FakeInterest que devolve sempre 1 e passa-o ao AccountService num teste.
:::

</details>

## O container de DI

```csharp
// Program.cs: register
builder.Services.AddScoped<IInterestCalculator,
    PromoInterest>();
builder.Services.AddScoped<AccountService>();

// the controller receives the service
public AccountsController(AccountService service)
{
    _service = service;
}
```

- O container cria os objetos e entrega-os a quem os pede.
- AddScoped\<TInterface, TImpl\> diz qual implementar.
- O construtor declara o que a classe precisa.
- Nunca se faz new de um serviço.

<details>
<summary>Saber mais</summary>

O container de DI é uma fábrica configurável. No Program.cs dizes 'quando alguém pedir IInterestCalculator, entrega PromoInterest'. O ASP.NET Core cria o controller por cada pedido, olha para o construtor e resolve cada parâmetro recursivamente.

Trocar de implementação é mudar uma linha de registo. O resto do código não se altera.

:::caution[Armadilha]
Registar a classe mas esquecer-se de registar uma das suas dependências. O erro surge em execução, no primeiro pedido.
:::

</details>

## Tempos de vida

| Tempo de vida | Instância | Exemplo típico |
| --- | --- | --- |
| Transient | Nova de cada vez que é pedida | Serviços leves e sem estado |
| Scoped | Uma por pedido HTTP | DbContext e serviços de aplicação |
| Singleton | Uma para toda a aplicação | Caches e clientes partilhados |

:::caution[Atenção]
Atenção: um Singleton não deve depender de um Scoped, porque viveria mais tempo do que a dependência e ficaria com um objeto já descartado.
:::

<details>
<summary>Saber mais</summary>

Transient cria uma instância nova de cada vez. Scoped cria uma por pedido HTTP, e é o tempo de vida do DbContext. Singleton cria uma para toda a aplicação.

Um Singleton nunca deve receber um Scoped no construtor: viveria mais do que a sua dependência, que já teria sido descartada.

:::caution[Armadilha]
Singleton que depende do DbContext. Dá erro de validação do container, ou pior, partilha um DbContext entre pedidos.
:::

</details>

## Logging e opções também se injetam

```csharp
public class AccountService
{
    private readonly ILogger<AccountService> _log;
    private readonly InterestOptions _options;

    public AccountService(
        ILogger<AccountService> log,
        IOptions<InterestOptions> options)
    {
        _log = log;
        _options = options.Value;
    }
}
```

- ILogger\<T\> regista mensagens com nível e categoria.
- IOptions\<T\> dá acesso à configuração tipada.
- Mensagens com marcadores, como \{Number\}, ficam pesquisáveis.
- Os serviços do framework usam o mesmo mecanismo.

<details>
<summary>Saber mais</summary>

ILogger\<T\> regista mensagens com nível (Information, Warning, Error) e categoria (o tipo T). Usa marcadores nomeados, como \{Number\}, em vez de concatenar: o texto fica constante e os valores ficam pesquisáveis nos sistemas de logs.

IOptions\<T\> liga uma secção do appsettings a uma classe tipada.

</details>

## Boas práticas

#### Depender de interfaces

Pedir IInterestCalculator e não PromoInterest: trocar a implementação não obriga a alterar a classe.

#### Poucas dependências

Um construtor com sete parâmetros é sinal de que a classe faz demasiado.

#### Sem new nos serviços

Se uma classe cria o que usa, não se consegue substituir nem testar sozinha.

#### Sem GetService

Pedir ao container dentro do código esconde as dependências. Usar o construtor.

<details>
<summary>Saber mais</summary>

Um construtor com sete parâmetros é um sinal: a classe provavelmente faz demasiado. GetService dentro do código (service locator) esconde as dependências e dificulta os testes. O construtor é o sítio honesto para declarar do que a classe precisa.

</details>

## Juros injetados

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Contrato.** IInterestCalculator, com as implementações StandardInterest e PromoInterest
2. **Registar.** a implementação no Program.cs com AddScoped
3. **Injetar.** o calculador num AccountService e usá-lo no POST para devolver os juros anuais
4. **Configurar.** a taxa em appsettings.json, lida com IOptions
5. **Registar no log.** o número da conta e os juros calculados com ILogger

<details>
<summary>Ver resultado esperado</summary>

```text
POST /api/accounts
{ "balance": 1000.00 }

201 Created
{
  "number": "AC-001",
  "annualInterest": 20.00
}
```

</details>

:::note[Extra]
Escolher a implementação por configuração (Standard ou Promo) sem recompilar.
:::

<details>
<summary>Saber mais</summary>

Só passas ao capítulo seguinte quando o resultado esperado aparecer no teu computador. Se algo falhar, lê a mensagem de erro de baixo para cima: a última linha costuma dizer o que correu mal.

:::tip[Experimenta]
Escolher a implementação por configuração (Basic or Discounted) sem recompilar.
:::

</details>
