---
title: "Mini-aplicação de consola"
description: "O enunciado de uma aplicação de consola completa, para juntar tudo o que aprendeste."
sidebar:
  order: 4
---

O enunciado de uma aplicação de consola completa, para juntar tudo o que aprendeste.

## Enunciado: gestão de contas

#### Contexto

Um banco quer uma aplicação de consola para registar contas e consultar totais por cliente. Os dados ficam em memória enquanto o programa corre.

```csharp
1) Criar conta
2) Listar contas
3) Total por cliente
0) Sair
```

#### Funcionalidades

- 1 · Criar conta: pede o número, o nome e o NIF do cliente e o saldo inicial.
- 2 · Listar contas: mostra número, cliente e saldo, do maior para o menor.
- 3 · Total por cliente: mostra a soma dos saldos de cada cliente.
- 0 · Sair: termina o programa.

<details>
<summary>Saber mais</summary>

Tudo fica em memória enquanto o programa corre: não há base de dados neste módulo. Decide tu a ordem em que implementas as opções do menu. Uma sugestão: começa pela 1 e pela 2, porque a 3 depende de ter contas criadas.

:::tip[Experimenta]
Antes de escreveres código, desenha as classes que vais precisar e a estrutura de dados onde guardas as contas.
:::

</details>

## Enunciado: regras e estrutura

#### Regras de validação

- O número da conta não pode estar vazio nem repetido.
- O NIF tem 9 dígitos.
- O saldo inicial é um número maior ou igual a zero.
- Uma opção inválida mostra uma mensagem e volta ao menu.
- Uma entrada inválida nunca faz o programa terminar.

#### Estrutura obrigatória

- Uma class Customer e um record Account.
- As contas guardadas numa List\<Account\>.
- LINQ nas opções 2 e 3.
- Um método para cada opção do menu.

## Enunciado: exemplo de execução

#### Exemplo de execução

```csharp
=== Contas ===
1) Criar conta
2) Listar contas
3) Total por cliente
0) Sair
> 1
Número: AC-001
Cliente: Ana Pereira
NIF: 123456789
Saldo inicial: 320,50
Conta criada.
> 3
Ana Pereira: 320,50
```

#### Extras (opcional)

- Pesquisar uma conta pelo número, com um Dictionary.
- Calcular os juros com a interface IInterestCalculator.
- Impedir dois clientes com o mesmo NIF.

<details>
<summary>Saber mais</summary>

Reproduz o exemplo exatamente, incluindo o formato do saldo com duas casas e vírgula decimal. Os extras são opcionais, mas o de impedir NIFs repetidos obriga-te a pensar num Dictionary.

</details>

## Antes de terminar

#### Critérios de conclusão

- Compila sem avisos
- Cumpre todos os requisitos do enunciado
- Trata entradas inválidas sem rebentar
- O formando explica uma classe e uma consulta LINQ do seu código

#### Perguntas de «porquê»

- Porque usámos decimal e não double?
- Porque é que Account é um record?
- O que acontece se o e-mail for null?

<details>
<summary>Saber mais</summary>

O critério de explicar uma classe e uma consulta LINQ do teu código é o mais importante: mostra que percebes o que escreveste.

</details>
