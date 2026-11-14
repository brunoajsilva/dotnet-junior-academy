---
title: "Objetos e coleções"
description: "Como representar o domínio de um banco com classes, records, interfaces e coleções."
sidebar:
  order: 2
---

Como representar o domínio de um banco com classes, records, interfaces e coleções.

## Classes e records

```csharp
public class Customer
{
    public string Name { get; }
    public string TaxId { get; }

    public Customer(string name, string nif)
    {
        Name = name;
        TaxId = nif;
    }
}

public record Account(
    string Number,
    Customer AccountHolder,
    decimal Balance);
```

- class: identidade e comportamento.
- record: dados imutáveis, igualdade por valor.
- Propriedades \{ get; \} em vez de campos ou métodos públicos;

<details>
<summary>Saber mais</summary>

Uma class representa algo com identidade: duas contas com os mesmos dados continuam a ser dois objetos. Um record representa dados: dois records com os mesmos valores são iguais, e o ToString já mostra as propriedades.

Usa record para valores e DTOs; usa class para entidades com comportamento e estado que muda.

:::tip[Experimenta]
Cria o mesmo tipo como class e como record, instancia dois objetos iguais e compara-os com ==.
:::

</details>

## Classes: get, set, init e private set

```csharp
public class Customer
{
    public string Name { get; set; }    // read and write
    public string TaxId { get; init; }   // only on creation
    public int Points { get; private set; } // only the class

    private string _email = "";
    public string Email
    {
        get => _email;
        set => _email = value.Trim();
    }

    public void AddPoints(int n) => Points += n;
}

var c = new Customer { Name = "Ana", TaxId = "1" };
c.Name = "Ana P.";  // c.TaxId = "2" does not compile
```

- get lê; set escreve.
- init só permite escrever ao criar o objeto.
- private set protege o estado: só a classe o altera.
- O set pode validar ou normalizar o valor.

<details>
<summary>Saber mais</summary>

Propriedades são a forma de expor estado. get lê, set escreve, init só deixa escrever na criação do objeto. private set é a escolha para estado que só a própria classe pode alterar, com validação.

Assim, o objeto garante que nunca fica num estado inválido: quem o usa não consegue pôr um saldo negativo.

:::caution[Armadilha]
Propriedades públicas com set para tudo. A classe perde o controlo sobre as suas próprias regras.
:::

</details>

## Classes: Interfaces

```csharp
public interface IInterestCalculator
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
}
```

- Interface: diz o quê (os métodos), não como.
- Cada classe que a implementa cumpre o contrato à sua maneira.
- Quem usa a interface não sabe, nem precisa de saber, qual a classe concreta.
- Nome começa por I.

<details>
<summary>Saber mais</summary>

Uma interface é um contrato. IInterestCalculator diz que existe um método Calculate, mas não como. StandardInterest e PromoInterest cumprem o contrato de formas diferentes, e quem usa a interface não precisa de saber qual recebeu.

É esta ideia que mais à frente permite a Dependency Injection e os mocks nos testes.

:::tip[Experimenta]
Implementa duas classes de IInterestCalculator e escolhe uma por argumento da linha de comandos.
:::

</details>

## Classes: Composição em vez de herança

```csharp
public class InterestService
{
    private readonly IInterestCalculator _calculator;

    // composition: receives the calculator from outside
    public InterestService(IInterestCalculator calculator)
        => _calculator = calculator;

    public decimal Annual(Account a)
        => _calculator.Calculate(a);
}

var normal = new InterestService(new StandardInterest());
var promo = new InterestService(new PromoInterest(0.03m));
```

- Composição: a classe tem outra e delega-lhe trabalho.
- Herança: a classe é uma especialização e fica presa à base.
- Trocar o objeto recebido muda o comportamento.
- Base da Dependency Injection.

<details>
<summary>Saber mais</summary>

Composição significa 'tem um': a classe recebe outro objeto e delega-lhe trabalho. Herança significa 'é um' e fixa a classe à sua base. Em geral compõe-se, e herda-se só quando a relação 'é um' é verdadeira em qualquer situação.

Trocar o objeto recebido muda o comportamento sem tocar na classe, e é exatamente isso que a Dependency Injection automatiza.

</details>

## Coleções: List e Dictionary

```csharp
var ana = new Customer("Ana Pereira", "123456789");
var accounts = new List<Account>();
accounts.Add(new Account("AC-001", ana, 320.50m));

var byNumber = new Dictionary<string, Account>();
byNumber["AC-001"] = accounts[0];

if (byNumber.TryGetValue("AC-002", out var a))
    Console.WriteLine(a.Balance);
```

- List: sequência ordenada.
- Dictionary: acesso por chave.
- TryGetValue evita exceções.

<details>
<summary>Saber mais</summary>

List\<T\> mantém ordem e permite aceder por índice. Dictionary\<K,V\> procura por chave em tempo praticamente constante, ideal para encontrar uma conta pelo número.

O indexador dict\[key\] lança KeyNotFoundException se a chave não existir. TryGetValue devolve bool e preenche o valor, sem exceção.

:::caution[Armadilha]
Usar List e procurar com um ciclo quando a pesquisa é sempre por chave.
:::

</details>

## Genéricos

```csharp
public class Result<T>
{
    public bool Success { get; }
    public T? Value { get; }
    public string? Error { get; }

    public Result(T value)
        => (Success, Value) = (true, value);
    public Result(string error) => Error = error;
}

static T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;

var r = new Result<decimal>(320.5m);
var m = Max(3, 7);          // T is int
var p = Max("Ana", "Rui");  // T is string
```

- T é um tipo que se escolhe ao usar.
- List\<T\> e Dictionary\<K,V\> já são genéricos.
- where limita os tipos aceites.
- Um só código serve vários tipos, com verificação do compilador.

<details>
<summary>Saber mais</summary>

Um genérico é código escrito uma vez para vários tipos. List\<T\> funciona para List\<int\> e List\<Account\> com verificação do compilador. Com where podes exigir que T implemente uma interface ou tenha construtor sem parâmetros.

:::tip[Experimenta]
Escreve um método genérico Largest\<T\>(List\<T\> items) where T : IComparable\<T\>.
:::

</details>

## Modelar o domínio

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

| Entidade | Campos |
| --- | --- |
| Account | Number · Balance · Opened |
| AccountHolder | Customer · Since |
| Customer | Name · TaxId |

Relações: Account tem um AccountHolder; AccountHolder é um Customer.

1. Modelar Customer, Account e AccountHolder
2. Calcular os juros com IInterestCalculator
3. Guardar contas numa List e numa Dictionary
4. Experimentar com três contas de exemplo

<details>
<summary>Ver resultado esperado</summary>

```text
Compila sem avisos
Três contas criadas e listadas
```

</details>

<details>
<summary>Saber mais</summary>

AccountHolder (titular) é o cliente que contrata a conta. Neste modelo, AccountHolder é um Customer (herança) e a Account tem um AccountHolder (composição). Aceitam-se variações, desde que as duas relações estejam corretas.

:::tip[Experimenta]
Desenha primeiro as três classes num papel com as setas «tem um» e «é um». Só depois escreve o código.
:::

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

Qual a principal diferença entre record e class?

- **A.** O record não pode ter métodos
- **B.** O record compara por valor
- **C.** A class é mais rápida
- **D.** O record é sempre mutável

<details>
<summary>Ver resposta</summary>

**B. O record compara por valor**

Dois records com os mesmos valores são iguais. Duas instâncias de class só são iguais se forem o mesmo objeto.

</details>

### Pergunta 2

O que permite uma propriedade com init?

- **A.** Escrever em qualquer momento
- **B.** Escrever só ao criar o objeto
- **C.** Só ler
- **D.** Escrever apenas dentro da classe

<details>
<summary>Ver resposta</summary>

**B. Escrever só ao criar o objeto**

init só aceita atribuição na criação do objeto.

</details>

### Pergunta 3

Porque é que TryGetValue é preferível ao indexador de um Dictionary?

- **A.** É mais curto
- **B.** Não lança exceção se a chave não existir
- **C.** Ordena os valores
- **D.** Evita duplicados

<details>
<summary>Ver resposta</summary>

**B. Não lança exceção se a chave não existir**

O indexador lança KeyNotFoundException; TryGetValue devolve false.

</details>
