---
title: "OAuth 2.0 e OpenID Connect"
description: "Delegar acesso sem partilhar a password: os papéis, os fluxos e os tipos de token."
sidebar:
  order: 3
---

Delegar acesso sem partilhar a password: os papéis, os fluxos e os tipos de token.

## A ideia: delegar sem partilhar a password

#### Sem OAuth

- Uma aplicação de gestão de despesas pede o teu email e a password do banco.
- Fica com acesso a tudo, para sempre.

#### Com OAuth

- A aplicação envia-te ao banco para te autenticares lá.
- Recebe um token com acesso só às contas, durante 15 minutos.
- Podes revogá-lo sem mudar a password.

:::note[Nota]
OAuth 2.0 é um protocolo de autorização (delegação de acesso). Não define como o utilizador se autentica.
:::

<details>
<summary>Saber mais</summary>

A comparação clássica é a chave de manobrista: abre a porta e liga o carro, mas não abre a mala nem o porta-luvas, e podes recuperá-la a qualquer momento. O token OAuth é isso, para uma API.

</details>

## Os quatro papéis

#### Resource Owner

- O dono dos dados.
- O cliente do banco.

#### Client

- A aplicação que quer aceder.
- A app móvel, um site, outro serviço.

#### Authorization Server

- Autentica o utilizador e emite tokens.
- No projeto: a própria API. Num banco real: um servidor de identidade.

#### Resource Server

- A API que guarda os dados e valida os tokens.
- A BankingApp.

<details>
<summary>Saber mais</summary>

Em projetos pequenos, o Authorization Server e o Resource Server são a mesma aplicação, como acontece na BankingApp: a mesma API emite e valida o token. Em sistemas maiores são separados (Microsoft Entra ID, Keycloak, Auth0, Duende IdentityServer), e a API só valida tokens que outro emitiu.

</details>

## Authorization Code com PKCE

1. **Pedido** O cliente redireciona o utilizador para o Authorization Server.
2. **Login** O utilizador autentica-se lá e dá consentimento.
3. **Código** O servidor devolve um código de curta duração ao cliente.
4. **Troca** O cliente troca o código por tokens, provando que foi ele que começou (PKCE).
5. **Chamada** O cliente chama a API com o access token no cabeçalho Authorization.
6. **Validação** A API valida o token e responde.

:::note[Nota]
É o fluxo para aplicações com um utilizador: web, móvel e SPA.

O PKCE protege o código de ser roubado e usado por outra aplicação.
:::

<details>
<summary>Saber mais</summary>

O código passa pelo browser, onde pode ser intercetado. Por isso o cliente cria um segredo aleatório (code verifier), envia o seu hash no passo 1 (code challenge) e o segredo original no passo 4. Quem roubar o código não tem o segredo e não consegue trocá-lo por tokens.

O PKCE é hoje recomendado para todos os clientes, e não só para as apps móveis.

</details>

## Que fluxo usar?

| Cenário | Fluxo | Notas |
| --- | --- | --- |
| Site ou app com um utilizador a fazer login | Authorization Code + PKCE | O fluxo por omissão. |
| Um serviço a chamar outro, sem utilizador | Client Credentials | O cliente autentica-se com o seu id e segredo. |
| Dispositivo sem teclado (televisão) | Device Code | O utilizador autentica-se noutro dispositivo. |
| Aplicação própria que envia email e password | Password (ROPC) | Desaconselhado e removido do OAuth 2.1. |

:::caution[Atenção]
Na BankingApp, a API recebe o email e a password e emite o token. É uma simplificação para aprender o JWT; num sistema real, o login seria feito por um servidor de identidade.
:::

<details>
<summary>Saber mais</summary>

O Implicit Flow, usado antigamente por SPAs, também foi retirado: devolvia o token no URL. Hoje as SPAs usam o Authorization Code com PKCE.

</details>

## Os tokens

| Token | Para quê | Duração | Para quem |
| --- | --- | --- | --- |
| Access token | Chamar a API | Curta (minutos) | A API (Resource Server) |
| Refresh token | Pedir um novo access token sem novo login | Longa (dias) | O Authorization Server |
| ID token (OpenID Connect) | Dizer à aplicação quem é o utilizador | Curta | A aplicação cliente |

:::caution[Atenção]
O OpenID Connect (OIDC) é uma camada de identidade sobre o OAuth 2.0: acrescenta o ID token e o endpoint userinfo, para a aplicação saber quem fez login.
:::

<details>
<summary>Saber mais</summary>

O access token pode ser opaco (uma referência que a API pergunta ao servidor) ou um JWT (a API valida sozinha). O formato dos access tokens neste curso é o JWT, tema do capítulo seguinte.

:::caution[Armadilha]
Enviar o ID token à API. O ID token é para a aplicação cliente; a API só deve aceitar access tokens.
:::

</details>

## Basic Auth vs OAuth 2.0

|  | Basic Auth | OAuth 2.0 |
| --- | --- | --- |
| O que a API recebe | A password do utilizador | Um token |
| Quem vê a password | A API e todos os clientes | Só o Authorization Server |
| Duração do acesso | Até a password mudar | Limitada (minutos) |
| Âmbito do acesso | Tudo | Limitado por scopes |
| Revogação | Mudar a password | Revogar o token ou o refresh token |
| Autenticação multifator | Não suporta | Suportada no servidor de identidade |
| Complexidade | Muito baixa | Mais peças (servidor, fluxos, tokens) |
| Quando usar | Ferramentas internas, testes e serviços legados sobre HTTPS | APIs expostas a aplicações e utilizadores |

<details>
<summary>Saber mais</summary>

O custo do OAuth é a complexidade: mais peças, mais configuração. Em troca, a password nunca sai do Authorization Server e o acesso passa a ser limitado e revogável. Num banco, essa troca compensa sempre.

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

O OAuth 2.0 é, sobretudo, um protocolo de...

- **A.** Autenticação
- **B.** Autorização (delegação de acesso)
- **C.** Encriptação
- **D.** Compressão

<details>
<summary>Ver resposta</summary>

**B. Autorização (delegação de acesso)**

Define como uma aplicação obtém acesso limitado em nome do utilizador. A identidade vem do OpenID Connect.

</details>

### Pergunta 2

Que fluxo se usa por omissão numa aplicação com utilizador?

- **A.** Password
- **B.** Implicit
- **C.** Authorization Code com PKCE
- **D.** Basic

<details>
<summary>Ver resposta</summary>

**C. Authorization Code com PKCE**

Authorization Code com PKCE é o recomendado para web, móvel e SPA.

</details>

### Pergunta 3

Que fluxo usa um serviço a chamar outro, sem utilizador?

- **A.** Client Credentials
- **B.** Authorization Code
- **C.** Device Code
- **D.** Implicit

<details>
<summary>Ver resposta</summary>

**A. Client Credentials**

O cliente autentica-se com o seu próprio id e segredo.

</details>

### Pergunta 4

Para que serve o refresh token?

- **A.** Chamar a API
- **B.** Obter um novo access token sem novo login
- **C.** Encriptar a password
- **D.** Identificar o utilizador à API

<details>
<summary>Ver resposta</summary>

**B. Obter um novo access token sem novo login**

Permite que o access token seja curto sem obrigar a um novo login.

</details>

### Pergunta 5

O que acrescenta o OpenID Connect ao OAuth 2.0?

- **A.** Mais velocidade
- **B.** O ID token, para saber quem fez login
- **C.** Encriptação do tráfego
- **D.** Nada

<details>
<summary>Ver resposta</summary>

**B. O ID token, para saber quem fez login**

É a camada de identidade sobre o OAuth 2.0.

</details>
