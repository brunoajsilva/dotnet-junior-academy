---
title: "JWT por dentro"
description: "O formato do token que a BankingApp emite: três partes, claims e uma assinatura."
sidebar:
  order: 4
---

O formato do token que a BankingApp emite: três partes, claims e uma assinatura.

## Três partes

```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwibmFtZSI6IkFuYSJ9.kD3x...

# 1. header (base64url)
{ "alg": "HS256", "typ": "JWT" }

# 2. payload = the claims (base64url)
{
  "sub": "1",
  "name": "Ana Pereira",
  "role": "Customer",
  "iss": "AuthLab",
  "aud": "AuthLab.Clients",
  "iat": 1793690000,
  "exp": 1793693600
}

# 3. signature
HMACSHA256( base64url(header) + "." + base64url(payload), secretKey )
```

- Header, payload e assinatura, separados por pontos.
- Header e payload são JSON em base64url.
- Qualquer pessoa pode ler o payload.
- A assinatura impede que seja alterado.

<details>
<summary>Saber mais</summary>

Um JWT (JSON Web Token, pronuncia-se «jót») está assinado, não encriptado. A assinatura garante que o conteúdo não foi alterado e que foi emitido por quem tem a chave. Não esconde nada: podes colar o token em jwt.io e ler as claims.

Por isso nunca se põem passwords, números de cartão ou outros segredos no payload.

:::caution[Armadilha]
Achar que o JWT é secreto. Se um dado não pode ser lido pelo utilizador ou por quem intercete o token, não pertence ao payload.
:::

:::tip[Experimenta]
Corre o Login do AuthLab (capítulo seguinte), cola o accessToken em jwt.io e vê as claims. Altera um carácter do payload e vê a assinatura ficar inválida.
:::

</details>

## Claims registadas

| Claim | Nome | Significado |
| --- | --- | --- |
| sub | Subject | Quem é o utilizador (o id do cliente). |
| iss | Issuer | Quem emitiu o token. |
| aud | Audience | Para que API é o token. |
| exp | Expiration | Quando deixa de ser válido (segundos desde 1970, UTC). |
| iat | Issued at | Quando foi emitido. |
| nbf | Not before | Só é válido a partir daqui. |
| name, email, role | Personalizadas | Dados úteis à API. Mantém-nas poucas: o token vai em todos os pedidos. |

<details>
<summary>Saber mais</summary>

O payload cresce com cada claim, e o token viaja em todos os pedidos. Por isso incluem-se apenas o identificador e o que a API usa em quase todos os pedidos (papel, nome). Os restantes dados vão-se buscar à base de dados com o id do sub.

</details>

## Assinatura: simétrica ou assimétrica

|  | HS256 (simétrica) | RS256 (assimétrica) |
| --- | --- | --- |
| Chaves | Uma só, partilhada | Privada (assina) e pública (valida) |
| Quem assina | Quem tem a chave | Só o dono da chave privada |
| Quem valida | Quem tem a chave (e por isso também podia assinar) | Qualquer um com a chave pública |
| Ideal para | Uma API que emite e valida os seus tokens | Um servidor de identidade e várias APIs |
| Neste curso | Usada | Para saberes que existe |

<details>
<summary>Saber mais</summary>

Com HS256, qualquer serviço que valide o token tem a chave que também permite assinar tokens. Para uma API que emite e valida os seus tokens, como a BankingApp, é adequado e simples. Quando várias APIs validam tokens de um servidor de identidade, usa-se RS256: as APIs só têm a chave pública e não conseguem fabricar tokens.

</details>

## O que a API valida

#### Assinatura

- O token foi emitido por quem tem a chave?
- Foi alterado?

#### Emissor (iss)

Foi emitido por quem esperamos?

#### Audiência (aud)

É um token para esta API?

#### Validade (exp)

Ainda não expirou?

:::note[Nota]
No ASP.NET Core, estas quatro verificações configuram-se no TokenValidationParameters.

Se alguma falhar, a resposta é 401.
:::

<details>
<summary>Saber mais</summary>

A audiência evita que um token emitido para a API A seja aceite pela API B. O ClockSkew é a tolerância entre relógios, por omissão cinco minutos; no AuthLab pomos zero para veres a expiração a acontecer à hora certa.

:::caution[Armadilha]
Desligar ValidateIssuer, ValidateAudience ou ValidateLifetime para «fazer funcionar». O erro não desaparece: passa a ser uma falha de segurança.
:::

</details>

## O token não se revoga

#### O problema

- A API valida o token sozinha, sem perguntar a ninguém.
- Um token roubado funciona até expirar.

#### A resposta

- Access tokens curtos (minutos).
- Um refresh token para renovar, guardado no servidor e revogável.

:::note[Nota]
Expiração curta e refresh token são as duas metades da mesma solução.
:::

<details>
<summary>Saber mais</summary>

A vantagem do JWT (a API não precisa de ir à base de dados) é também a sua limitação (a API não sabe se o token foi revogado). Quando é mesmo preciso revogar já, mantém-se uma lista de tokens revogados e verifica-se em cada pedido, o que reintroduz a consulta que o JWT queria evitar.

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

O que garante a assinatura de um JWT?

- **A.** Que o conteúdo está encriptado
- **B.** Que o conteúdo não foi alterado
- **C.** Que o utilizador é maior de idade
- **D.** Que o token nunca expira

<details>
<summary>Ver resposta</summary>

**B. Que o conteúdo não foi alterado**

A assinatura prova a integridade e a origem. Não esconde o conteúdo.

</details>

### Pergunta 2

Qual destas informações NÃO deve estar no payload?

- **A.** O id do cliente
- **B.** O papel
- **C.** A password
- **D.** A hora de expiração

<details>
<summary>Ver resposta</summary>

**C. A password**

O payload é legível por qualquer pessoa. Segredos nunca entram.

</details>

### Pergunta 3

Para que serve a claim aud?

- **A.** Dizer para que API é o token
- **B.** Guardar a data de nascimento
- **C.** Identificar o utilizador
- **D.** Assinar o token

<details>
<summary>Ver resposta</summary>

**A. Dizer para que API é o token**

A audiência impede que um token de uma API seja aceite por outra.

</details>

### Pergunta 4

Porque se usam access tokens de curta duração?

- **A.** Para poupar memória
- **B.** Porque um token roubado deixa de servir quando expira
- **C.** Porque o JWT não aceita mais
- **D.** Para não precisar de HTTPS

<details>
<summary>Ver resposta</summary>

**B. Porque um token roubado deixa de servir quando expira**

A API não consegue revogar o token, por isso a expiração curta limita o estrago.

</details>
