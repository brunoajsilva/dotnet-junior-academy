---
title: "Projeto Final"
description: "Uma API de um banco, em 6 dias: montas a base com os passos guiados e depois decides, planeias e constróis sozinho."
sidebar:
  order: 0
  label: "Visão geral"
---

Uma API de um banco, em 6 dias: montas a base com os passos guiados e depois decides, planeias e constróis sozinho.

A BankingApp é uma Web API para um banco: clientes que se registam, fazem login e gerem as suas contas. Constróis a solução de raiz, com Clean Architecture, usando tudo o que aprendeste. No primeiro dia segues um guia. A partir do segundo, recebes um enunciado com muitas user stories e tens de planear o que consegues entregar.

### Como está organizado

Um dia guiado, uma introdução com o formador, quatro dias de user stories e um dia de entrega final.

<details>
<summary>Saber mais</summary>

No dia 1 segues o guia: a solução já funcional, com base de dados e Swagger, e a autenticação JWT. A introdução ao projeto, com o planeamento, é uma sessão à parte, conduzida pelo formador, que acontece antes de começares a construir. Nos dias 2 a 5 constróis as user stories que planeaste, sem código de apoio. No dia 6 entregas o projeto e fazemos uma review em conjunto.

</details>

### Mais trabalho do que tempo

O enunciado propõe mais user stories do que cabem em 6 dias. É de propósito.

<details>
<summary>Saber mais</summary>

Numa equipa real, o que está no backlog é sempre mais do que a capacidade. A competência que se treina aqui é escolher: estimar, priorizar e dizer «isto fica de fora». Ninguém espera que acabes tudo. Espera-se que entregues o que escolheste, bem feito, e que saibas explicar as tuas decisões.

</details>

### Como sabes que acabaste

As user stories do teu plano estão prontas, os testes passam e explicas o percurso de um pedido.

<details>
<summary>Saber mais</summary>

No dia 6 tens a lista de critérios de aceitação. Confirma que consegues demonstrar cada um, antes de entregares. Na review comparas o plano com o que realmente aconteceu: onde estimaste bem, onde falhaste e porquê.

</details>

## Os dias do projeto

| Dia | Tema | Objetivo |
| --- | --- | --- |
| Dia 1 | [Montar a solução e autenticação JWT](montar-a-solucao/) | Estrutura, EF Core, repositório e Swagger; depois Register e Login anónimos, RetrieveDashboard autenticado e a coleção do Bruno. |
| Dia 2 | [User stories](enunciado-user-stories/) | Executas o plano, começando pelas user stories mais arriscadas. Uma user story só está pronta com testes e um pedido no Bruno. |
| Dia 3 | [User stories](enunciado-user-stories/) | Continuas a executar o plano, sem código de apoio. |
| Dia 4 | [User stories](enunciado-user-stories/) | Continuas a executar o plano e a ajustá-lo quando a realidade o contradiz. |
| Dia 5 | [User stories e revisão do plano](enunciado-user-stories/) | A meio do dia revês o plano: o que atrasou? O que cortas? Atualizas e comunicas. |
| Dia 6 | [Entrega final](entrega-final/) | Entregas o projeto e fazemos a review em conjunto, com demonstração, perguntas e plano contra realidade. |

## Arquitetura

### BankingApp.Domain: Regras do negócio

**Contém:**

- Customer, Account e AccountStatus
- Transaction e as entidades das tuas user stories
- DomainException

**Referencia:** nenhum projeto.

**Nunca conhece:** EF Core, ASP.NET Core, ou qualquer outro projeto.

É o centro. As regras do banco (saldo, estado da conta, validações) vivem aqui. Como não referencia nada, é rápido de testar e impossível de contaminar com detalhes técnicos.

### BankingApp.Application: Casos de uso

**Contém:**

- Commands, queries e handlers
- ICustomerRepository, IPasswordHasher, ITokenService
- Request, Response, Error e IHandler
- AddApplication()

**Referencia:** BankingApp.Domain.

**Nunca conhece:** EF Core e ASP.NET Core.

Orquestra o Domain: por exemplo, o RegisterHandler verifica o email, cria o cliente e a primeira conta. As interfaces vivem aqui porque quem as usa é que define o contrato.

### BankingApp.Infrastructure: Detalhes técnicos

**Contém:**

- BankingAppContext, configurations e migrations
- Repositórios
- JwtTokenService e PasswordHasherService
- AddInfrastructure()

**Referencia:** BankingApp.Application.

**Nunca conhece:** A camada Api.

Implementa os contratos da Application com o EF Core e com as bibliotecas de segurança. Trocar de base de dados é escrever outra implementação aqui.

### BankingApp.Api: HTTP

**Contém:**

- Controllers e DTOs
- ExceptionMiddleware
- Configuração do JWT
- Program.cs e appsettings.json

**Referencia:** BankingApp.Application, BankingApp.Infrastructure.

**Nunca conhece:** Lógica de negócio.

Traduz HTTP em comandos e consultas, valida o token e devolve sempre um Response (HTTP 200). Referencia a Infrastructure só para a registar no container.

### BankingApp.Tests: Verificação

**Contém:**

- Testes do Domain
- Testes dos handlers com mocks

**Referencia:** BankingApp.Domain, BankingApp.Application.

**Nunca conhece:** Base de dados real.

Testa as regras e os handlers sem base de dados nem HTTP. Corre em segundos.

## O percurso de um pedido

1. **Pedido com token** (api): POST /api/dashboard/retrieve com o cabeçalho Authorization: Bearer \<token\>. O pedido entra no pipeline do ASP.NET Core.
2. **Middleware de autenticação** (api): UseAuthentication lê o token, valida a assinatura, o emissor, a audiência e a validade, e preenche o User com os claims. Se o token for inválido, \[Authorize\] responde 200 com o erro unauthorized e o pedido para aqui.
3. **Controller** (api): O RetrieveDashboard lê o claim sub (o id do cliente), cria a RetrieveDashboardQuery e chama o handler.
4. **Handler** (application): O RetrieveDashboardHandler pede o cliente com as contas ao repositório e calcula o saldo total. Se o cliente não existir, devolve Response.Fail com o erro not\_found.
5. **Repositório** (infrastructure): O CustomerRepository faz a consulta com Include e AsNoTracking, e o EF Core gera o SELECT com o JOIN.
6. **Resposta** (api): O controller converte os dados do Response em DashboardResponse (Map) e devolve-o, sempre com HTTP 200. Se os dados faltarem, vão os errors. Se uma exceção subir, o ExceptionMiddleware também responde 200, com um erro validation ou unexpected.

## Endpoints

| User story | Pedido | Acesso | Resultado (HTTP 200) | Erros possíveis |
| --- | --- | --- | --- | --- |
| Guia | POST /api/auth/register | anónimo | success (a primeira conta) | validation, conflict |
| Guia | POST /api/auth/login | anónimo | success (o token) | unauthorized |
| Guia | POST /api/dashboard/retrieve | token | success (o resumo) | unauthorized |
| US1 | POST /api/accounts/open | token | success (o número da conta) | validation, unauthorized, conflict |
| US2 | POST /api/accounts/list  ·  POST /api/accounts/get | token | success | unauthorized, not\_found |
| US3 | POST /api/accounts/close | token | success | unauthorized, not\_found, conflict |
| US4 | POST /api/accounts/deposit | token | success | validation, unauthorized, not\_found, conflict |
| US5 | POST /api/accounts/withdraw | token | success | validation, unauthorized, not\_found, conflict |
| US6 | POST /api/accounts/set-daily-limit | token | success | validation, unauthorized, not\_found |
| US7 | POST /api/transfers/create | token | success | validation, unauthorized, not\_found, conflict |
| US8 | POST /api/transfers/reverse | token | success | unauthorized, not\_found, conflict |
| US9 | POST /api/accounts/list-transactions | token | success (a página) | validation, unauthorized, not\_found |
| US10 | POST /api/dashboard/retrieve (completo) | token | success | unauthorized |
| US11 | POST /api/accounts/export-transactions | token | success (CSV) | validation, unauthorized, not\_found |
| US12 | POST /api/beneficiaries/add · list · remove | token | success | validation, unauthorized, not\_found, conflict |
| US13 | POST /api/payments/pay | token | success | validation, unauthorized, not\_found, conflict |
| US14 | POST /api/accounts/get-interest · apply-interest | token | success | unauthorized, not\_found, conflict |
| US15 | POST /api/loans/simulate | token | success | validation, unauthorized |
| US16 | POST /api/loans/request · list · cancel | token | success | unauthorized, not\_found, conflict |
| US17 | POST /api/profile/get  ·  POST /api/profile/change-password | token | success | validation, unauthorized |
| US18 | POST /api/auth/refresh | anónimo | success | unauthorized |
| US19 | POST /api/auth/logout | anónimo | success | validation |
| US20 | POST /api/auth/login (limite) | anónimo | success | unauthorized, rate\_limited |

## Critérios de aceitação

- [ ] Entreguei um plano com estimativas, riscos, dependências e o que ficou de fora
- [ ] Revi o plano a meio do projeto e sei explicar o que mudou
- [ ] A solução compila sem avisos e todos os testes passam
- [ ] O Domain não referencia nenhum projeto nem pacote do EF Core
- [ ] As migrations criam todas as tabelas e os índices únicos
- [ ] Sei explicar porque é que, num projeto real, a chave do JWT não ficaria no appsettings.json
- [ ] Os endpoints anónimos funcionam sem token e os restantes devolvem o erro unauthorized sem token
- [ ] Nenhum cliente consegue ver ou mexer em contas de outro cliente
- [ ] Todas as respostas, incluindo as de erro, chegam num Response com HTTP 200, nunca como exceção sem tratamento
- [ ] Os saldos nunca ficam desalinhados com os movimentos, mesmo quando algo falha
- [ ] Os logs não têm passwords nem tokens
- [ ] Cada user story que entreguei tem testes e um pedido no Bruno
- [ ] Consigo explicar o percurso de um pedido, do cabeçalho Authorization à base de dados
- [ ] Comparei o estimado com o real e sei o que aprendi

## Extras

- Alterar o plano para incluir uma user story que ficou de fora e estimar o quanto demoraria
- Acrescentar um endpoint de saúde (/health) que verifica a ligação à base de dados
