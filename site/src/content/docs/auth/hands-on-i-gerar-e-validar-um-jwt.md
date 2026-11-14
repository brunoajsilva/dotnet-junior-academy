---
title: "Hands-on I: gerar e validar um JWT"
description: "Constróis de raiz uma Web API pequena, o AuthLab: configuras a autenticação JWT, crias no controller um método que gera o token e outro que só responde a quem o enviar. Não é a BankingApp: serve para perceberes cada peça antes do projeto."
sidebar:
  order: 5
---

Constróis de raiz uma Web API pequena, o AuthLab: configuras a autenticação JWT, crias no controller um método que gera o token e outro que só responde a quem o enviar. Não é a BankingApp: serve para perceberes cada peça antes do projeto.

## Criar o projeto

```bash
dotnet new webapi --use-controllers -n AuthLab
cd AuthLab

dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer

# remove the template sample (WeatherForecast) and keep only Program.cs
```

- dotnet new webapi --use-controllers cria uma Web API com controllers.
- O pacote JwtBearer valida tokens.
- A chave tem de ter pelo menos 32 caracteres para HS256.

<details>
<summary>Saber mais</summary>

Neste laboratório a chave fica no appsettings.json, para simplificar. Em produção, a mesma chave vem de uma variável de ambiente ou de um cofre (Azure Key Vault, por exemplo): o código lê sempre de builder.Configuration e não sabe a diferença.

:::caution[Armadilha]
Copiar a chave do laboratório para um projeto real. Quem a tiver consegue fabricar tokens válidos.
:::

</details>

## Configuração

```json
{
  "Jwt": {
    "Issuer": "AuthLab",
    "Audience": "AuthLab.Clients",
    "Key": "a-random-text-with-at-least-32-characters-here",
    "ExpiresMinutes": 15
  },
  "Logging": { "LogLevel": { "Default": "Information", "Microsoft.AspNetCore": "Warning" } },
  "AllowedHosts": "*"
}
```

- Issuer e Audience identificam quem emite e quem recebe o token.
- A chave (Jwt:Key) assina o token e tem pelo menos 32 caracteres.
- ExpiresMinutes controla a validade do token.
- Tudo fica na secção Jwt, lida pelo builder.Configuration.

## Program.cs: configurar a autenticação

```csharp
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

// the "Jwt" section (appsettings.json) becomes an object the controller can receive
var jwt = builder.Configuration.GetSection("Jwt").Get<JwtSettings>()!;
builder.Services.AddSingleton(jwt);

builder.Services.AddControllers();

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.MapInboundClaims = false;                // keep "sub" as "sub"
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,           ValidIssuer = jwt.Issuer,
            ValidateAudience = true,         ValidAudience = jwt.Audience,
            ValidateIssuerSigningKey = true, IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwt.Key)),
            ValidateLifetime = true,         ClockSkew = TimeSpan.Zero
        };
    });
builder.Services.AddAuthorization();

var app = builder.Build();

app.UseHttpsRedirection();
app.UseAuthentication();   // who are you?
app.UseAuthorization();    // can you do this?
app.MapControllers();

app.Run();

// JwtSettings.cs
public class JwtSettings
{
    public string Issuer { get; set; } = "";
    public string Audience { get; set; } = "";
    public string Key { get; set; } = "";
    public int ExpiresMinutes { get; set; } = 15;
}
```

- A secção Jwt passa a um objeto JwtSettings, registado no container.
- AddJwtBearer configura as quatro validações.
- UseAuthentication e UseAuthorization na ordem certa.
- MapControllers expõe os controllers.

<details>
<summary>Saber mais</summary>

O MapInboundClaims = false evita que o ASP.NET Core renomeie as claims do token (por exemplo, sub passaria a ser um nome comprido da Microsoft). Assim, o que vês no jwt.io é o que lês no código.

Registar o JwtSettings no container (AddSingleton) permite ao controller recebê-lo no construtor, tal como qualquer outro serviço. É a mesma Dependency Injection que já usaste.

:::caution[Armadilha]
Trocar a ordem do UseAuthentication e do UseAuthorization. Todos os métodos protegidos passam a responder 401.
:::

</details>

## AuthController: gerar o token e usá-lo

```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;

[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    // in-memory users: only for this lab (a real API stores a password HASH)
    private static readonly List<User> Users =
    [
        new(1, "ana@example.com", "Passw0rd!", "Ana Pereira", "Customer"),
        new(2, "rui@example.com", "Passw0rd!", "Rui Costa", "Manager")
    ];

    private readonly JwtSettings _jwt;

    public AuthController(JwtSettings jwt) => _jwt = jwt;

    // 1. generates the token: anonymous, because the caller does not have one yet
    [AllowAnonymous]
    [HttpPost("login")]
    public ActionResult<LoginResponse> Login(LoginRequest body)
    {
        var user = Users.FirstOrDefault(u => u.Email == body.Email && u.Password == body.Password);
        if (user is null) return Unauthorized();   // same answer for unknown email and wrong password

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim("name", user.Name),
            new Claim("role", user.Role)
        };
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwt.Key));
        var expires = DateTime.UtcNow.AddMinutes(_jwt.ExpiresMinutes);

        var token = new JwtSecurityToken(_jwt.Issuer, _jwt.Audience, claims, expires: expires,
            signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));

        return Ok(new LoginResponse(new JwtSecurityTokenHandler().WriteToken(token), expires));
    }

    // 2. authenticated: without a valid token the answer is 401
    [Authorize]
    [HttpGet("me")]
    public IActionResult Me() => Ok(new
    {
        id = User.FindFirstValue("sub"),
        name = User.FindFirstValue("name"),
        role = User.FindFirstValue("role")
    });
}

public record LoginRequest(string Email, string Password);
public record LoginResponse(string AccessToken, DateTime ExpiresAtUtc);
public record User(int Id, string Email, string Password, string Name, string Role);
```

- Login é anónimo e gera o token, com as claims sub, name e role.
- Me tem \[Authorize\]: só responde com um token válido.
- A identidade vem do token: User.FindFirstValue("sub").
- O Login devolve o mesmo 401 para email desconhecido e password errada.

<details>
<summary>Saber mais</summary>

Este exemplo guarda as passwords em texto dentro da lista, só para o laboratório ser pequeno. A BankingApp guarda um hash (capítulo 7), e a criação do token vive numa classe própria (JwtTokenService), em vez de estar no controller.

O \[AllowAnonymous\] no Login é explícito de propósito: quando mais tarde protegeres o controller inteiro com \[Authorize\], o Login continua a funcionar.

:::caution[Armadilha]
Pôr \[Authorize\] no Login. Ninguém consegue obter o primeiro token.
:::

:::tip[Experimenta]
Acrescenta uma claim email ao token e devolve-a no Me.
:::

</details>

## Bruno: o cabeçalho Authorization

#### O ambiente

- Cria o ambiente Local com a variável baseUrl.
- Usa o endereço https que o dotnet run escreve.
- Seleciona o ambiente no canto superior direito.

#### Pedido de login

- Novo pedido POST para \{\{baseUrl\}\}/api/auth/login.
- Body em JSON com email e password.
- Separador Vars, Post Response: token = res.body.accessToken.

#### Pedido autenticado

- GET \{\{baseUrl\}\}/api/auth/me.
- No separador Auth escolhe «Bearer Token» e escreve \{\{token\}\}.
- O Bruno envia o cabeçalho Authorization: Bearer \<token\>.

#### Pedido sem token

- Duplica o pedido anterior e põe o separador Auth em «No Auth».
- A resposta é 401: prova que o \[Authorize\] está a funcionar.

<details>
<summary>Saber mais</summary>

O Bruno guarda as coleções em ficheiros de texto (.bru), que podes pôr no repositório e rever em Pull Requests. A variável token é preenchida automaticamente a cada Login, por isso não copias o token à mão.

:::caution[Armadilha]
Deixar o separador Auth em «No Auth» no pedido protegido. A API responde 401 e parece um erro do servidor.
:::

</details>

## Experimentar o AuthLab

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Arrancar.** correr dotnet run e anotar o endereço https
2. **Sem token.** GET /api/auth/me devolve 401
3. **Login.** POST /api/auth/login com ana@example.com e Passw0rd! devolve o accessToken
4. **Com token.** GET /api/auth/me com o Bearer Token devolve 200 com o id, nome e papel
5. **Descodificar.** colar o token em jwt.io e identificar sub, name, role, iss, aud e exp
6. **Adulterar.** alterar um carácter do token e confirmar que o Me responde 401
7. **Expirar.** mudar ExpiresMinutes para 1, fazer login, esperar 61 segundos e confirmar o 401

:::tip[Dica]
Se o Me responde sempre 401, confirma a ordem do UseAuthentication e do UseAuthorization e se a chave do appsettings.json não mudou entre arranques.
:::

<details>
<summary>Ver resultado esperado</summary>

```text
GET  /api/auth/me (sem token)      -> 401
POST /api/auth/login               -> 200 { accessToken, expiresAtUtc }
GET  /api/auth/me (com token)      -> 200 { id: "1", name: "Ana Pereira", role: "Customer" }
GET  /api/auth/me (token alterado) -> 401
GET  /api/auth/me (token expirado) -> 401
```

</details>

:::note[Extra]
Troca o ClockSkew por 5 minutos e vê o token continuar válido depois de expirar.
:::

<details>
<summary>Saber mais</summary>

O passo «Adulterar» é o mais importante: mostra que a API não confia no conteúdo do token, confia na assinatura. Sem a chave, ninguém fabrica um token válido.

:::tip[Experimenta]
Troca uma letra no meio do payload (a segunda parte) e volta a chamar o Me.
:::

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

Onde fica a chave de assinatura durante o desenvolvimento?

- **A.** Num cofre ou numa variável de ambiente
- **B.** No código-fonte
- **C.** No nome do projeto
- **D.** Num comentário

<details>
<summary>Ver resposta</summary>

**A. Num cofre ou numa variável de ambiente**

Fora do repositório. Num laboratório pode ficar no appsettings.json, mas em produção vem de variáveis de ambiente ou de um cofre.

</details>

### Pergunta 2

O que devolve o método Me se o token tiver um carácter alterado?

- **A.** 200
- **B.** 401
- **C.** 403
- **D.** 500

<details>
<summary>Ver resposta</summary>

**B. 401**

A assinatura deixa de bater certo e a autenticação falha: 401.

</details>

### Pergunta 3

Porque tem o Login o atributo \[AllowAnonymous\]?

- **A.** Para ser mais rápido
- **B.** Porque quem faz login ainda não tem token
- **C.** Porque o JWT o exige
- **D.** Para devolver 403

<details>
<summary>Ver resposta</summary>

**B. Porque quem faz login ainda não tem token**

O Login é o método que gera o primeiro token, por isso não pode exigir um.

</details>

### Pergunta 4

O que faz o atributo \[Authorize\] num método do controller?

- **A.** Valida a password
- **B.** Exige um utilizador autenticado
- **C.** Emite o token
- **D.** Encripta a resposta

<details>
<summary>Ver resposta</summary>

**B. Exige um utilizador autenticado**

Sem utilizador autenticado, a resposta é 401.

</details>
