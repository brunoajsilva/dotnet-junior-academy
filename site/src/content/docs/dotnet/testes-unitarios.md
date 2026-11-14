---
title: "Testes unitários"
description: "Provar que o código funciona com testes rápidos e isolados."
sidebar:
  order: 5
---

Provar que o código funciona com testes rápidos e isolados.

## A pirâmide de testes

- **Ponta a ponta**: poucos, lentos
- **Integração**: alguns
- **Unitários**: muitos, rápidos

#### Unitário

- Uma classe ou método isolado, sem base de dados nem rede.

#### Integração

- Várias peças reais juntas, como a API e a base de dados.

#### Ponta a ponta

- O sistema completo, como um utilizador o usa.

## O primeiro teste com xUnit

```csharp
public class PromoInterestTests
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
}
```

- \[Fact\] marca um teste.
- Arrange: preparar os objetos.
- Act: executar o que se testa.
- Assert: verificar o resultado.

<details>
<summary>Saber mais</summary>

Um teste unitário segue três passos: Arrange (preparar), Act (executar), Assert (verificar). \[Fact\] marca o método como teste. Um bom teste lê-se como uma frase: dado este contexto, quando fizer isto, então acontece aquilo.

</details>

## Vários casos: Theory

```csharp
[Theory]
[InlineData(0, 200, 0)]
[InlineData(2, 200, 4)]
[InlineData(5, 200, 10)]
public void Calculate_AppliesRate(
    int ratePercent, int balance, int expected)
{
    var calc = new PromoInterest(ratePercent / 100m);
    var acc = new Account("AC-001", ana, balance);

    Assert.Equal(expected, calc.Calculate(acc));
}
```

- \[Theory\] corre o mesmo teste com vários dados.
- \[InlineData\] fornece cada caso.
- Cada caso aparece como um teste separado.
- Bom para limites e valores especiais.

<details>
<summary>Saber mais</summary>

\[Theory\] corre o mesmo teste com vários dados fornecidos por \[InlineData\]. Cada caso aparece como teste separado no relatório. É a ferramenta certa para valores-limite: 0, 1, o máximo, o valor negativo.

</details>

## Verificações úteis

```csharp
Assert.Equal(180m, result);
Assert.True(account.IsActive);
Assert.False(list.Any());
Assert.Null(result);
Assert.Contains("AC-001", numbers);
Assert.Empty(list);

// exceptions
var ex = Assert.Throws<InvalidAccountException>(
    () => new Account("AC-001", ana, -5m));
Assert.Equal("AC-001", ex.Number);
```

- Cada Assert verifica uma coisa.
- Throws confirma que a exceção certa é lançada.
- O teste falha à primeira verificação que falhar.
- Para exceções assíncronas, usar ThrowsAsync.

<details>
<summary>Saber mais</summary>

Assert.Equal, True, False, Null, Contains, Single... cada um verifica uma coisa. Assert.Throws\<T\> confirma que um código lança a exceção certa; para métodos async usa Assert.ThrowsAsync\<T\> com await.

</details>

## Isolar dependências com mocks

```csharp
var repo = Substitute.For<IAccountRepository>();
repo.GetAsync("AC-001")
    .Returns(new Account("AC-001", ana, 200m));

var service = new AccountService(
    repo, new PromoInterest(0.02m));

var interest = await service.CalculateAsync("AC-001");

Assert.Equal(4m, interest);
await repo.Received(1).GetAsync("AC-001");
```

- Um mock é um objeto falso que substitui uma dependência.
- Define o que devolve e verifica como foi chamado.
- O serviço é testado sem base de dados.
- Só funciona porque a dependência é uma interface.

<details>
<summary>Saber mais</summary>

Um mock substitui uma dependência por um objeto falso que controlas: defines o que devolve e depois verificas como foi chamado. Com NSubstitute, Substitute.For\<IAccountRepository\>() cria o falso. Só funciona porque a dependência é uma interface, e é por isso que a Dependency Injection e os testes andam juntos.

</details>

## Boas práticas

#### Nomes que explicam

Method\_Scenario\_Result: ao ver o nome de um teste que falha, percebe-se o problema.

#### Um comportamento por teste

Se um teste falha, deve ser óbvio o que partiu. Evitar testes longos.

#### Independentes e rápidos

Sem ordem entre testes, sem base de dados e sem rede. Devem correr em segundos.

#### Testar o teu código

Não testar o framework: confiar que o EF e o ASP.NET Core fazem o que prometem.

<details>
<summary>Saber mais</summary>

Method\_Scenario\_Result, por exemplo Calculate\_PromoRate\_ReturnsInterest. Quando este teste falhar no CI, o nome já diz o que se partiu, sem abrir o código.

</details>

## Testar o saldo

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Três testes.** \[Fact\] para PromoInterest: taxa 0%, 2% e 5%
2. **Um Theory.** com \[InlineData\] para os mesmos cálculos
3. **Uma exceção.** InvalidAccountException para um saldo negativo
4. **Um mock.** do repositório para testar o AccountService

<details>
<summary>Ver resultado esperado</summary>

```text
dotnet test

Passed!  - Failed:     0,
           Passed:     8,
           Skipped:    0,
           Total:      8
```

</details>

:::note[Extra]
Gerar o relatório de cobertura de testes e identificar uma classe sem testes. Dica: nuget dotnet-reportgenerator
:::

<details>
<summary>Saber mais</summary>

Só passas ao capítulo seguinte quando o resultado esperado aparecer no teu computador. Se algo falhar, lê a mensagem de erro de baixo para cima: a última linha costuma dizer o que correu mal.

:::tip[Experimenta]
Gerar o relatório de cobertura de testes e identificar uma classe sem testes. Dica: nuget dotnet-reportgenerator
:::

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

O que representa o 'Arrange' num teste?

- **A.** Executar o código
- **B.** Preparar os objetos e os dados
- **C.** Verificar o resultado
- **D.** Limpar a base de dados

<details>
<summary>Ver resposta</summary>

**B. Preparar os objetos e os dados**

Arrange, Act, Assert: preparar, executar, verificar.

</details>

### Pergunta 2

Quando usar \[Theory\] em vez de \[Fact\]?

- **A.** Quando o teste é lento
- **B.** Quando o mesmo teste corre com vários dados
- **C.** Quando há exceções
- **D.** Quando há mocks

<details>
<summary>Ver resposta</summary>

**B. Quando o mesmo teste corre com vários dados**

\[InlineData\] fornece cada caso e cada um aparece como teste separado.

</details>

### Pergunta 3

Porque é que um mock exige que a dependência seja uma interface?

- **A.** Por regra do xUnit
- **B.** Porque é preciso poder substituí-la por um falso
- **C.** Porque o EF o exige
- **D.** Não exige

<details>
<summary>Ver resposta</summary>

**B. Porque é preciso poder substituí-la por um falso**

Sem interface (ou método virtual), não há como substituir a implementação.

</details>
