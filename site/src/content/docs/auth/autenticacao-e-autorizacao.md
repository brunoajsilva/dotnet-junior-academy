---
title: "Autenticação e autorização"
description: "Duas perguntas diferentes que se confundem: quem és? E o que podes fazer?"
sidebar:
  order: 1
---

Duas perguntas diferentes que se confundem: quem és? E o que podes fazer?

## Duas perguntas diferentes

#### Autenticação

- Quem és?
- Verificar a identidade com uma password, um token ou um certificado.
- Se falha: 401 Unauthorized.

#### Autorização

- O que podes fazer?
- Decidir o que uma identidade já conhecida pode fazer.
- Se falha: 403 Forbidden.

:::note[Nota]
A autenticação vem sempre primeiro: só se decide o que alguém pode fazer depois de saber quem é.

Num banco: o login autentica a Ana. Ver a conta da Ana é uma decisão de autorização.
:::

<details>
<summary>Saber mais</summary>

Uma imagem útil: o seguro de um hotel. Na receção mostras o cartão de cidadão e recebes um cartão de quarto (autenticação). O cartão só abre a tua porta, e não a dos outros quartos nem a do cofre (autorização).

Em inglês aparecem as abreviaturas AuthN (authentication) e AuthZ (authorization). Quando alguém diz «auth» sem mais, pergunta qual das duas.

:::caution[Armadilha]
Chamar «não autorizado» ao 401. O nome do código HTTP é Unauthorized, mas significa «não autenticado». O 403 é que significa «sei quem és e não podes».
:::

</details>

## 401 ou 403?

| Situação | Código | Porquê |
| --- | --- | --- |
| Pedido sem token | 401 | Não sabemos quem é. |
| Token expirado ou com a assinatura alterada | 401 | A identidade não foi provada. |
| Cliente a chamar um endpoint só de gestores | 403 | Sabemos quem é, e o papel não chega. |
| Cliente a pedir a conta de outro cliente | 404 | Responder 404 em vez de 403 não revela que a conta existe. |
| Email ou password errados no login | 401 | A mesma resposta para os dois casos, para não revelar que emails existem. |

:::caution[Atenção]
O 401 pede que te voltes a autenticar. O 403 não adianta voltar a tentar com as mesmas credenciais.
:::

<details>
<summary>Saber mais</summary>

O 404 para recursos de outros utilizadores é uma decisão de segurança: com o 403 estás a confirmar que o recurso existe. Num banco, confirmar que um número de conta existe já é informação a mais.

</details>

## Onde entra no pipeline

```csharp
var app = builder.Build();

app.UseHttpsRedirection();

app.UseAuthentication();   // 1. who are you?  Reads the credentials and builds the User
app.UseAuthorization();    // 2. can you do this?  Checks [Authorize] against the User

app.MapControllers();
app.Run();
```

- UseAuthentication lê as credenciais e preenche o User.
- UseAuthorization decide, com o User já preenchido.
- A ordem importa: a autorização depende da autenticação.
- Ambos vêm antes do MapControllers.

<details>
<summary>Saber mais</summary>

Se trocares a ordem, a autorização corre com um utilizador anónimo e todos os endpoints protegidos respondem 401, mesmo com um token válido. É um erro clássico: o token está certo, o pipeline é que está pela ordem errada.

:::caution[Armadilha]
Esquecer o UseAuthentication. O \[Authorize\] passa a responder sempre 401.
:::

</details>

## Identidade, claims e papéis

#### Claim

- Uma afirmação sobre o utilizador.
- Par nome-valor: name = Ana Pereira.

#### ClaimsPrincipal

- O User no ASP.NET Core.
- Agrupa as claims de uma identidade.

#### Role (papel)

- Um grupo de permissões: Customer, Manager.
- É só uma claim especial.

#### Policy

- Uma regra com nome.
- Combina papéis e claims: «gestor do departamento de crédito».

<details>
<summary>Saber mais</summary>

Depois de a autenticação correr, o ASP.NET Core constrói um ClaimsPrincipal com as claims do token. Tudo o que se segue (papéis, políticas, o id do cliente) lê desse objeto.

Um papel é uma claim com um tipo reconhecido como «role». Uma policy é uma regra com nome que podes reutilizar em vários endpoints.

</details>
