---
title: "Hands-on II: autorização"
description: "Com o token a funcionar, decide-se o que cada utilizador pode fazer: papéis, políticas e dados que só pertencem ao dono. Continuas no AuthLab."
sidebar:
  order: 6
---

Com o token a funcionar, decide-se o que cada utilizador pode fazer: papéis, políticas e dados que só pertencem ao dono. Continuas no AuthLab.

## Papéis (roles)

```csharp
// Program.cs, inside AddJwtBearer
options.TokenValidationParameters = new TokenValidationParameters
{
    // ...same as before, plus:
    NameClaimType = "name",    // User.Identity.Name reads this claim
    RoleClaimType = "role"     // [Authorize(Roles = ...)] and User.IsInRole read this claim
};

// AdminController.cs
[ApiController]
[Route("api/admin")]
public class AdminController : ControllerBase
{
    [Authorize(Roles = "Manager")]
    [HttpGet("customers")]
    public IActionResult ListCustomers() => Ok(new[] { "Ana Pereira", "Rui Costa" });
}
```

- O token já leva a claim role.
- RoleClaimType diz ao ASP.NET Core qual claim é o papel.
- \[Authorize(Roles = ...)\] protege o método.
- Papel errado: 403.

<details>
<summary>Saber mais</summary>

Sem RoleClaimType = "role", o ASP.NET Core procura a claim com o nome comprido da Microsoft e nunca encontra o papel: todos os pedidos dão 403, mesmo para o gestor.

:::caution[Armadilha]
Papéis a mais. Quando os papéis passam de três ou quatro, reparas que estás a combinar regras: é a altura de usar policies.
:::

</details>

## Políticas (policies)

```csharp
// Program.cs
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanReviewLoans", p => p
        .RequireRole("Manager")
        .RequireClaim("department", "Credit"))
    .AddPolicy("VerifiedEmail", p => p
        .RequireClaim("email_verified", "true"));

// LoansController.cs
[Authorize(Policy = "CanReviewLoans")]
[HttpPost("{id}/approve")]
public IActionResult Approve(int id) => NoContent();
```

- Uma policy tem nome e agrupa regras.
- RequireRole e RequireClaim combinam-se.
- Reutiliza-se em vários métodos.
- Muda-se num sítio só.

<details>
<summary>Saber mais</summary>

As policies também aceitam requisitos próprios (IAuthorizationRequirement e AuthorizationHandler), para regras que não são «tem esta claim», por exemplo «só entre as 9h e as 18h». Para as regras deste curso, RequireRole e RequireClaim chegam.

</details>

## O recurso é teu?

```csharp
[Authorize]
[HttpGet("{number}")]
public IActionResult GetAccount(string number)
{
    var customerId = int.Parse(User.FindFirstValue("sub")!);
    var account = Accounts.FirstOrDefault(a => a.Number == number);

    // the account is not yours? Answer exactly as if it did not exist
    if (account is null || account.CustomerId != customerId)
        return NotFound();

    return Ok(account);
}
```

- O id vem do token, nunca do pedido.
- Verifica que o recurso pertence ao utilizador.
- Se não pertence: 404, como se não existisse.
- Papéis e policies não chegam para isto.

<details>
<summary>Saber mais</summary>

Papéis dizem «os clientes podem consultar contas». Não dizem «esta conta é tua». A verificação de propriedade faz-se no código, depois de carregar o recurso. É a falha de segurança mais frequente em APIs (a OWASP chama-lhe Broken Object Level Authorization): trocar o número na URL e ver a conta de outra pessoa.

:::caution[Armadilha]
Receber o customerId no corpo ou na URL. Quem faz o pedido pode pôr lá qualquer valor.
:::

</details>

## Refresh token: renovar sem novo login

```http
POST /login
  -> { "accessToken": "eyJ...", "expiresAtUtc": "...in 15 min",
       "refreshToken": "a1b2c3..." }                      # long-lived, random, stored hashed on the server

# 15 minutes later the access token expires: the API answers 401

POST /refresh   { "refreshToken": "a1b2c3..." }
  -> { "accessToken": "eyJ...(new)", "refreshToken": "d4e5f6...(new)" }
     # the old refresh token is now invalid (rotation)

POST /logout    { "refreshToken": "d4e5f6..." }
  -> 204                                                  # the server deletes it: the session is over
```

- Access token curto, refresh token longo.
- O refresh token é aleatório e guardado no servidor (com hash).
- Cada renovação troca o refresh token por um novo (rotation).
- O logout apaga-o no servidor.

<details>
<summary>Saber mais</summary>

Guardar o refresh token no servidor é o que permite revogar: apagas a linha e a sessão acaba. O access token continua válido até expirar, e é por isso que é curto.

Guarda o refresh token com hash, tal como as passwords: se alguém ler a base de dados, não consegue usá-los.

</details>

## Papéis e dados do dono no AuthLab

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Claims.** configurar NameClaimType e RoleClaimType no TokenValidationParameters
2. **Gestores.** criar o AdminController com GET /api/admin/customers só para o papel Manager
3. **Policy.** criar a policy CanReviewLoans (papel Manager) e usá-la em POST /api/loans/\{id\}/approve
4. **Dono.** criar uma lista de contas com CustomerId e GET /api/accounts/\{number\} que devolve 404 às contas de outros
5. **Testar.** repetir os pedidos como ana (Customer) e como rui (Manager) e preencher a tabela de resultados

| Pedido | Sem token | Ana (Customer) | Rui (Manager) |
| --- | --- | --- | --- |
| GET /api/admin/customers | 401 | 403 | 200 |
| POST /api/loans/1/approve | 401 | 403 | 204 |
| GET /api/accounts/AC-001 (conta da Ana) | 401 | 200 | 404 |
| GET /api/accounts/AC-002 (conta do Rui) | 401 | 404 | 200 |

<details>
<summary>Ver resultado esperado</summary>

```text
Sem token -> 401 em todos
Customer num método de gestor -> 403
Conta de outro utilizador -> 404
```

</details>

:::note[Extra]
Acrescenta uma claim email\_verified e uma policy VerifiedEmail.
:::

<details>
<summary>Saber mais</summary>

Se a tabela de resultados te sair diferente, é quase sempre uma de três causas: o RoleClaimType em falta (tudo 403), a ordem UseAuthentication/UseAuthorization (tudo 401) ou o id lido do sítio errado.

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

Um Customer chama um método só para Manager. Que código recebe?

- **A.** 401
- **B.** 403
- **C.** 404
- **D.** 200

<details>
<summary>Ver resposta</summary>

**B. 403**

Está autenticado, mas o papel não chega: 403.

</details>

### Pergunta 2

De onde deve vir o id do cliente numa consulta às suas contas?

- **A.** Do corpo do pedido
- **B.** Da URL
- **C.** Do token
- **D.** De um cabeçalho personalizado

<details>
<summary>Ver resposta</summary>

**C. Do token**

Do token assinado. Tudo o que vem no pedido pode ser forjado.

</details>

### Pergunta 3

Para que serve uma policy?

- **A.** Guardar a password
- **B.** Agrupar regras de autorização com um nome reutilizável
- **C.** Emitir tokens
- **D.** Encriptar a ligação

<details>
<summary>Ver resposta</summary>

**B. Agrupar regras de autorização com um nome reutilizável**

Combina papéis e claims numa regra com nome, usada em vários métodos.

</details>

### Pergunta 4

Porque se guarda o refresh token no servidor?

- **A.** Para o poder revogar
- **B.** Para o tornar mais curto
- **C.** Porque o JWT o exige
- **D.** Para poupar espaço

<details>
<summary>Ver resposta</summary>

**A. Para o poder revogar**

Apagar o refresh token termina a sessão. Um access token não se consegue revogar.

</details>
