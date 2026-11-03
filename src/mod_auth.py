# -*- coding: utf-8 -*-
# Module 4: Autenticação e Autorização (Basic vs OAuth 2.0, JWT hands-on). Code in English.

def L(id, t, type, more=None, **kw):
    d = dict(id=id, t=t, type=type, **kw)
    if more: d['more'] = more
    return d

def Q(q, o, a, w): return dict(q=q, o=o, a=a, w=w)

# ------------------------------------------------------------------ code
PIPE = r'''var app = builder.Build();

app.UseHttpsRedirection();

app.UseAuthentication();   // 1. who are you?  Reads the credentials and builds the User
app.UseAuthorization();    // 2. can you do this?  Checks [Authorize] against the User

app.MapControllers();
app.Run();'''

BASIC_SH = r'''# the client joins "user:password" and encodes it in base64
echo -n 'ana@example.com:Passw0rd!' | base64
# YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==

# the header sent on EVERY request
Authorization: Basic YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==

# base64 is an encoding, not encryption: anyone can reverse it
echo 'YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==' | base64 -d
# ana@example.com:Passw0rd!

# curl does the same with -u
curl -u 'ana@example.com:Passw0rd!' https://localhost:5001/api/dashboard'''

JWT_DECODED = r'''eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwibmFtZSI6IkFuYSJ9.kD3x...

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
HMACSHA256( base64url(header) + "." + base64url(payload), secretKey )'''

LAB_SH = r'''dotnet new webapi --use-controllers -n AuthLab
cd AuthLab

dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer

# remove the template sample (WeatherForecast) and keep only Program.cs'''

LAB_SETTINGS = r'''{
  "Jwt": {
    "Issuer": "AuthLab",
    "Audience": "AuthLab.Clients",
    "Key": "a-random-text-with-at-least-32-characters-here",
    "ExpiresMinutes": 15
  },
  "Logging": { "LogLevel": { "Default": "Information", "Microsoft.AspNetCore": "Warning" } },
  "AllowedHosts": "*"
}'''

LAB_PROGRAM = r'''using System.Text;
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
}'''

LAB_CONTROLLER = r'''using System.IdentityModel.Tokens.Jwt;
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
public record User(int Id, string Email, string Password, string Name, string Role);'''

ROLE_CFG = r'''// Program.cs, inside AddJwtBearer
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
}'''

POLICY = r'''// Program.cs
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanReviewLoans", p => p
        .RequireRole("Manager")
        .RequireClaim("department", "Credit"))
    .AddPolicy("VerifiedEmail", p => p
        .RequireClaim("email_verified", "true"));

// LoansController.cs
[Authorize(Policy = "CanReviewLoans")]
[HttpPost("{id}/approve")]
public IActionResult Approve(int id) => NoContent();'''

OWNER = r'''[Authorize]
[HttpGet("{number}")]
public IActionResult GetAccount(string number)
{
    var customerId = int.Parse(User.FindFirstValue("sub")!);
    var account = Accounts.FirstOrDefault(a => a.Number == number);

    // the account is not yours? Answer exactly as if it did not exist
    if (account is null || account.CustomerId != customerId)
        return NotFound();

    return Ok(account);
}'''

HASH = r'''using Microsoft.AspNetCore.Identity;

var hasher = new PasswordHasher<object>();

// at registration: store ONLY the hash
string hash = hasher.HashPassword(null!, "Passw0rd!");
// "AQAAAAIAAYagAAAAE..."  (random salt included, different every time)

// at login: compare the typed password with the stored hash
var result = hasher.VerifyHashedPassword(null!, hash, "Passw0rd!");
bool ok = result != PasswordVerificationResult.Failed;'''

REFRESH_FLOW = r'''POST /login
  -> { "accessToken": "eyJ...", "expiresAtUtc": "...in 15 min",
       "refreshToken": "a1b2c3..." }                      # long-lived, random, stored hashed on the server

# 15 minutes later the access token expires: the API answers 401

POST /refresh   { "refreshToken": "a1b2c3..." }
  -> { "accessToken": "eyJ...(new)", "refreshToken": "d4e5f6...(new)" }
     # the old refresh token is now invalid (rotation)

POST /logout    { "refreshToken": "d4e5f6..." }
  -> 204                                                  # the server deletes it: the session is over'''

BRUNO_LAB = [
 dict(t="O ambiente", d=["Cria o ambiente Local com a variável baseUrl.", "Usa o endereço https que o dotnet run escreve.", "Seleciona o ambiente no canto superior direito."]),
 dict(t="Pedido de login", d=["Novo pedido POST para {{baseUrl}}/api/auth/login.", "Body em JSON com email e password.", "Separador Vars, Post Response: token = res.body.accessToken."]),
 dict(t="Pedido autenticado", d=["GET {{baseUrl}}/api/auth/me.", "No separador Auth escolhe «Bearer Token» e escreve {{token}}.", "O Bruno envia o cabeçalho Authorization: Bearer <token>."]),
 dict(t="Pedido sem token", d=["Duplica o pedido anterior e põe o separador Auth em «No Auth».", "A resposta é 401: prova que o [Authorize] está a funcionar."]),
]

# ------------------------------------------------------------------ chapters
C1 = dict(id="auth-1", t="Autenticação e autorização", intro="Duas perguntas diferentes que se confundem: quem és? E o que podes fazer?",
 lessons=[
  L("au-1-1", "Duas perguntas diferentes", "cards", items=[
     dict(t="Autenticação", d=["Quem és?", "Verificar a identidade com uma password, um token ou um certificado.", "Se falha: 401 Unauthorized."]),
     dict(t="Autorização", d=["O que podes fazer?", "Decidir o que uma identidade já conhecida pode fazer.", "Se falha: 403 Forbidden."]),
     dict(t="", d=["A autenticação vem sempre primeiro: só se decide o que alguém pode fazer depois de saber quem é.", "Num banco: o login autentica a Ana. Ver a conta da Ana é uma decisão de autorização."], note=True)],
    more=dict(more="Uma imagem útil: o seguro de um hotel. Na receção mostras o cartão de cidadão e recebes um cartão de quarto (autenticação). O cartão só abre a tua porta, e não a dos outros quartos nem a do cofre (autorização).\n\nEm inglês aparecem as abreviaturas AuthN (authentication) e AuthZ (authorization). Quando alguém diz «auth» sem mais, pergunta qual das duas.", pit="Chamar «não autorizado» ao 401. O nome do código HTTP é Unauthorized, mas significa «não autenticado». O 403 é que significa «sei quem és e não podes».")),
  L("au-1-2", "401 ou 403?", "table", rows=[
     ["Situação", "Código", "Porquê"],
     ["Pedido sem token", "401", "Não sabemos quem é."],
     ["Token expirado ou com a assinatura alterada", "401", "A identidade não foi provada."],
     ["Cliente a chamar um endpoint só de gestores", "403", "Sabemos quem é, e o papel não chega."],
     ["Cliente a pedir a conta de outro cliente", "404", "Responder 404 em vez de 403 não revela que a conta existe."],
     ["Email ou password errados no login", "401", "A mesma resposta para os dois casos, para não revelar que emails existem."]],
    note="O 401 pede que te voltes a autenticar. O 403 não adianta voltar a tentar com as mesmas credenciais.",
    more=dict(more="O 404 para recursos de outros utilizadores é uma decisão de segurança: com o 403 estás a confirmar que o recurso existe. Num banco, confirmar que um número de conta existe já é informação a mais.")),
  L("au-1-3", "Onde entra no pipeline", "code", lang="cs", code=PIPE,
    points=["UseAuthentication lê as credenciais e preenche o User.", "UseAuthorization decide, com o User já preenchido.", "A ordem importa: a autorização depende da autenticação.", "Ambos vêm antes do MapControllers."],
    more=dict(more="Se trocares a ordem, a autorização corre com um utilizador anónimo e todos os endpoints protegidos respondem 401, mesmo com um token válido. É um erro clássico: o token está certo, o pipeline é que está pela ordem errada.", pit="Esquecer o UseAuthentication. O [Authorize] passa a responder sempre 401.")),
  L("au-1-4", "Identidade, claims e papéis", "cards", items=[
     dict(t="Claim", d=["Uma afirmação sobre o utilizador.", "Par nome-valor: name = Ana Pereira."]),
     dict(t="ClaimsPrincipal", d=["O User no ASP.NET Core.", "Agrupa as claims de uma identidade."]),
     dict(t="Role (papel)", d=["Um grupo de permissões: Customer, Manager.", "É só uma claim especial."]),
     dict(t="Policy", d=["Uma regra com nome.", "Combina papéis e claims: «gestor do departamento de crédito»."])],
    more=dict(more="Depois de a autenticação correr, o ASP.NET Core constrói um ClaimsPrincipal com as claims do token. Tudo o que se segue (papéis, políticas, o id do cliente) lê desse objeto.\n\nUm papel é uma claim com um tipo reconhecido como «role». Uma policy é uma regra com nome que podes reutilizar em vários endpoints.")),
 ],
 quiz=[
  Q("Um pedido chega sem token a um endpoint protegido. Que código devolve a API?", ["200", "401", "403", "404"], 1, "Sem token não sabemos quem é: é um problema de autenticação, 401."),
  Q("Um cliente autenticado chama um endpoint só para gestores. Que código?", ["401", "403", "404", "500"], 1, "Sabemos quem é, mas o papel não chega: 403 Forbidden."),
  Q("Qual é a ordem correta no Program.cs?", ["UseAuthorization, UseAuthentication", "UseAuthentication, UseAuthorization", "Tanto faz", "Só é preciso UseAuthorization"], 1, "Primeiro identificas (autenticação), depois decides (autorização)."),
  Q("Porque devolve o sistema 404 para a conta de outro cliente?", ["Para poupar um pedido", "Para não revelar que a conta existe", "Porque o 403 não existe", "Porque a base de dados falhou"], 1, "Um 403 confirmaria que o recurso existe. O 404 trata-o como se não existisse."),
 ])

C2 = dict(id="auth-2", t="Basic Authentication", intro="O mecanismo mais simples: enviar o utilizador e a password em cada pedido. Percebe porque deixou de ser suficiente.",
 lessons=[
  L("au-2-1", "Como funciona", "cards", flow=3, items=[
     dict(t="Pedido", d=["O cliente chama um endpoint protegido sem credenciais."]),
     dict(t="Desafio", d=["A API responde 401 com o cabeçalho WWW-Authenticate: Basic."]),
     dict(t="Credenciais", d=["O cliente repete o pedido com Authorization: Basic base64(user:password)."]),
     dict(t="", d=["O servidor valida o utilizador e a password em todos os pedidos.", "Não há sessão nem token: as credenciais viajam sempre."], note=True)],
    more=dict(more="O Basic Auth faz parte do próprio protocolo HTTP (RFC 7617). É suportado por qualquer cliente HTTP sem código adicional, o que o torna útil em ferramentas internas e em testes rápidos.")),
  L("au-2-2", "O cabeçalho por dentro", "code", lang="sh", code=BASIC_SH,
    points=["O valor é «user:password» em base64.", "Base64 é uma codificação, não encriptação.", "Qualquer pessoa que veja o pedido recupera a password.", "O cabeçalho vai em todos os pedidos."],
    more=dict(more="Por isso o Basic só é aceitável sobre HTTPS. Mesmo assim, a password sai do cliente em cada pedido e passa por proxies, logs e ferramentas de depuração que registam cabeçalhos.", tryit="Corre o primeiro comando com uma password tua e depois o segundo comando para a recuperar. Dá para sentir o problema.")),
  L("au-2-3", "Os limites do Basic Auth", "table", rows=[
     ["Problema", "Consequência"],
     ["A password viaja em todos os pedidos", "Mais oportunidades de ser intercetada ou registada em logs."],
     ["A API vê a password do utilizador", "Uma aplicação de terceiros teria de receber a tua password do banco."],
     ["Não expira", "Só deixa de funcionar se mudares a password."],
     ["Sem âmbito (scope)", "Quem tem as credenciais pode fazer tudo."],
     ["Sem revogação parcial", "Para cortar o acesso a uma aplicação tens de mudar a password, e todas as outras aplicações perdem acesso."],
     ["Sem autenticação multifator", "Não há onde encaixar um segundo fator."]],
    more=dict(more="Estes limites são a razão de ser do OAuth 2.0: dar a uma aplicação um acesso limitado, temporário e revogável, sem lhe entregar a password.")),
  L("au-2-4", "Descodificar um cabeçalho Basic", "exercise",
    steps=[dict(lead="Codificar", text="gerar o base64 de «rui@example.com:Passw0rd!» com o comando echo -n ... | base64"),
           dict(lead="Descodificar", text="recuperar o texto original com base64 -d"),
           dict(lead="Pedido", text="com curl -u, chamar https://httpbin.org/basic-auth/rui/pass e ver a resposta 401 ou 200"),
           dict(lead="Concluir", text="escrever numa frase porque é que o Basic Auth não serve para uma aplicação móvel de um banco")],
    expected="rui@example.com:Passw0rd!\n\n(a descodificação devolve exatamente o texto original)",
    hint="Se estiveres no Windows, usa o Git Bash ou o PowerShell: [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(\"rui@example.com:Passw0rd!\")).",
    more=dict(more="O objetivo é sentires que o base64 não protege nada. Se conseguires descodificar em dois segundos, qualquer pessoa também consegue."))
 ],
 quiz=[
  Q("O que protege o base64 do cabeçalho Basic?", ["A password, porque é cifrada", "Nada: é só uma codificação reversível", "O utilizador, porque é anónimo", "O servidor, porque valida o tamanho"], 1, "Base64 não é segurança. Qualquer pessoa o descodifica."),
  Q("Com que frequência são enviadas as credenciais no Basic Auth?", ["Só no primeiro pedido", "Em todos os pedidos", "Uma vez por hora", "Nunca"], 1, "Não há sessão nem token: o cabeçalho vai em todos os pedidos."),
  Q("Qual destes é um limite do Basic Auth?", ["Não funciona em HTTPS", "A aplicação cliente tem de conhecer a password", "É demasiado lento", "Só funciona com .NET"], 1, "A aplicação cliente guarda e envia a password do utilizador, e não há acesso limitado nem revogável."),
 ])

C3 = dict(id="auth-3", t="OAuth 2.0 e OpenID Connect", intro="Delegar acesso sem partilhar a password: os papéis, os fluxos e os tipos de token.",
 lessons=[
  L("au-3-1", "A ideia: delegar sem partilhar a password", "cards", items=[
     dict(t="Sem OAuth", d=["Uma aplicação de gestão de despesas pede o teu email e a password do banco.", "Fica com acesso a tudo, para sempre."]),
     dict(t="Com OAuth", d=["A aplicação envia-te ao banco para te autenticares lá.", "Recebe um token com acesso só às contas, durante 15 minutos.", "Podes revogá-lo sem mudar a password."]),
     dict(t="", d=["OAuth 2.0 é um protocolo de autorização (delegação de acesso). Não define como o utilizador se autentica."], note=True)],
    more=dict(more="A comparação clássica é a chave de manobrista: abre a porta e liga o carro, mas não abre a mala nem o porta-luvas, e podes recuperá-la a qualquer momento. O token OAuth é isso, para uma API.")),
  L("au-3-2", "Os quatro papéis", "cards", items=[
     dict(t="Resource Owner", d=["O dono dos dados.", "O cliente do banco."]),
     dict(t="Client", d=["A aplicação que quer aceder.", "A app móvel, um site, outro serviço."]),
     dict(t="Authorization Server", d=["Autentica o utilizador e emite tokens.", "No projeto: a própria API. Num banco real: um servidor de identidade."]),
     dict(t="Resource Server", d=["A API que guarda os dados e valida os tokens.", "A BankingApp."])],
    more=dict(more="Em projetos pequenos, o Authorization Server e o Resource Server são a mesma aplicação, como acontece na BankingApp: a mesma API emite e valida o token. Em sistemas maiores são separados (Microsoft Entra ID, Keycloak, Auth0, Duende IdentityServer), e a API só valida tokens que outro emitiu.")),
  L("au-3-3", "Authorization Code com PKCE", "cards", flow=6, items=[
     dict(t="1. Pedido", d=["O cliente redireciona o utilizador para o Authorization Server."]),
     dict(t="2. Login", d=["O utilizador autentica-se lá e dá consentimento."]),
     dict(t="3. Código", d=["O servidor devolve um código de curta duração ao cliente."]),
     dict(t="4. Troca", d=["O cliente troca o código por tokens, provando que foi ele que começou (PKCE)."]),
     dict(t="5. Chamada", d=["O cliente chama a API com o access token no cabeçalho Authorization."]),
     dict(t="6. Validação", d=["A API valida o token e responde."]),
     dict(t="", d=["É o fluxo para aplicações com um utilizador: web, móvel e SPA.", "O PKCE protege o código de ser roubado e usado por outra aplicação."], note=True)],
    more=dict(more="O código passa pelo browser, onde pode ser intercetado. Por isso o cliente cria um segredo aleatório (code verifier), envia o seu hash no passo 1 (code challenge) e o segredo original no passo 4. Quem roubar o código não tem o segredo e não consegue trocá-lo por tokens.\n\nO PKCE é hoje recomendado para todos os clientes, e não só para as apps móveis.")),
  L("au-3-4", "Que fluxo usar?", "table", rows=[
     ["Cenário", "Fluxo", "Notas"],
     ["Site ou app com um utilizador a fazer login", "Authorization Code + PKCE", "O fluxo por omissão."],
     ["Um serviço a chamar outro, sem utilizador", "Client Credentials", "O cliente autentica-se com o seu id e segredo."],
     ["Dispositivo sem teclado (televisão)", "Device Code", "O utilizador autentica-se noutro dispositivo."],
     ["Aplicação própria que envia email e password", "Password (ROPC)", "Desaconselhado e removido do OAuth 2.1."]],
    note="Na BankingApp, a API recebe o email e a password e emite o token. É uma simplificação para aprender o JWT; num sistema real, o login seria feito por um servidor de identidade.",
    more=dict(more="O Implicit Flow, usado antigamente por SPAs, também foi retirado: devolvia o token no URL. Hoje as SPAs usam o Authorization Code com PKCE.")),
  L("au-3-5", "Os tokens", "table", rows=[
     ["Token", "Para quê", "Duração", "Para quem"],
     ["Access token", "Chamar a API", "Curta (minutos)", "A API (Resource Server)"],
     ["Refresh token", "Pedir um novo access token sem novo login", "Longa (dias)", "O Authorization Server"],
     ["ID token (OpenID Connect)", "Dizer à aplicação quem é o utilizador", "Curta", "A aplicação cliente"]],
    note="O OpenID Connect (OIDC) é uma camada de identidade sobre o OAuth 2.0: acrescenta o ID token e o endpoint userinfo, para a aplicação saber quem fez login.",
    more=dict(more="O access token pode ser opaco (uma referência que a API pergunta ao servidor) ou um JWT (a API valida sozinha). O formato dos access tokens neste curso é o JWT, tema do capítulo seguinte.", pit="Enviar o ID token à API. O ID token é para a aplicação cliente; a API só deve aceitar access tokens.")),
  L("au-3-6", "Basic Auth vs OAuth 2.0", "table", rows=[
     ["", "Basic Auth", "OAuth 2.0"],
     ["O que a API recebe", "A password do utilizador", "Um token"],
     ["Quem vê a password", "A API e todos os clientes", "Só o Authorization Server"],
     ["Duração do acesso", "Até a password mudar", "Limitada (minutos)"],
     ["Âmbito do acesso", "Tudo", "Limitado por scopes"],
     ["Revogação", "Mudar a password", "Revogar o token ou o refresh token"],
     ["Autenticação multifator", "Não suporta", "Suportada no servidor de identidade"],
     ["Complexidade", "Muito baixa", "Mais peças (servidor, fluxos, tokens)"],
     ["Quando usar", "Ferramentas internas, testes e serviços legados sobre HTTPS", "APIs expostas a aplicações e utilizadores"]],
    more=dict(more="O custo do OAuth é a complexidade: mais peças, mais configuração. Em troca, a password nunca sai do Authorization Server e o acesso passa a ser limitado e revogável. Num banco, essa troca compensa sempre.")),
 ],
 quiz=[
  Q("O OAuth 2.0 é, sobretudo, um protocolo de...", ["Autenticação", "Autorização (delegação de acesso)", "Encriptação", "Compressão"], 1, "Define como uma aplicação obtém acesso limitado em nome do utilizador. A identidade vem do OpenID Connect."),
  Q("Que fluxo se usa por omissão numa aplicação com utilizador?", ["Password", "Implicit", "Authorization Code com PKCE", "Basic"], 2, "Authorization Code com PKCE é o recomendado para web, móvel e SPA."),
  Q("Que fluxo usa um serviço a chamar outro, sem utilizador?", ["Client Credentials", "Authorization Code", "Device Code", "Implicit"], 0, "O cliente autentica-se com o seu próprio id e segredo."),
  Q("Para que serve o refresh token?", ["Chamar a API", "Obter um novo access token sem novo login", "Encriptar a password", "Identificar o utilizador à API"], 1, "Permite que o access token seja curto sem obrigar a um novo login."),
  Q("O que acrescenta o OpenID Connect ao OAuth 2.0?", ["Mais velocidade", "O ID token, para saber quem fez login", "Encriptação do tráfego", "Nada"], 1, "É a camada de identidade sobre o OAuth 2.0."),
 ])

C4 = dict(id="auth-4", t="JWT por dentro", intro="O formato do token que a BankingApp emite: três partes, claims e uma assinatura.",
 lessons=[
  L("au-4-1", "Três partes", "code", lang="sh", code=JWT_DECODED,
    points=["Header, payload e assinatura, separados por pontos.", "Header e payload são JSON em base64url.", "Qualquer pessoa pode ler o payload.", "A assinatura impede que seja alterado."],
    more=dict(more="Um JWT (JSON Web Token, pronuncia-se «jót») está assinado, não encriptado. A assinatura garante que o conteúdo não foi alterado e que foi emitido por quem tem a chave. Não esconde nada: podes colar o token em jwt.io e ler as claims.\n\nPor isso nunca se põem passwords, números de cartão ou outros segredos no payload.", pit="Achar que o JWT é secreto. Se um dado não pode ser lido pelo utilizador ou por quem intercete o token, não pertence ao payload.", tryit="Corre o Login do AuthLab (capítulo seguinte), cola o accessToken em jwt.io e vê as claims. Altera um carácter do payload e vê a assinatura ficar inválida.")),
  L("au-4-2", "Claims registadas", "table", rows=[
     ["Claim", "Nome", "Significado"],
     ["sub", "Subject", "Quem é o utilizador (o id do cliente)."],
     ["iss", "Issuer", "Quem emitiu o token."],
     ["aud", "Audience", "Para que API é o token."],
     ["exp", "Expiration", "Quando deixa de ser válido (segundos desde 1970, UTC)."],
     ["iat", "Issued at", "Quando foi emitido."],
     ["nbf", "Not before", "Só é válido a partir daqui."],
     ["name, email, role", "Personalizadas", "Dados úteis à API. Mantém-nas poucas: o token vai em todos os pedidos."]],
    more=dict(more="O payload cresce com cada claim, e o token viaja em todos os pedidos. Por isso incluem-se apenas o identificador e o que a API usa em quase todos os pedidos (papel, nome). Os restantes dados vão-se buscar à base de dados com o id do sub.")),
  L("au-4-3", "Assinatura: simétrica ou assimétrica", "table", rows=[
     ["", "HS256 (simétrica)", "RS256 (assimétrica)"],
     ["Chaves", "Uma só, partilhada", "Privada (assina) e pública (valida)"],
     ["Quem assina", "Quem tem a chave", "Só o dono da chave privada"],
     ["Quem valida", "Quem tem a chave (e por isso também podia assinar)", "Qualquer um com a chave pública"],
     ["Ideal para", "Uma API que emite e valida os seus tokens", "Um servidor de identidade e várias APIs"],
     ["Neste curso", "Usada", "Para saberes que existe"]],
    more=dict(more="Com HS256, qualquer serviço que valide o token tem a chave que também permite assinar tokens. Para uma API que emite e valida os seus tokens, como a BankingApp, é adequado e simples. Quando várias APIs validam tokens de um servidor de identidade, usa-se RS256: as APIs só têm a chave pública e não conseguem fabricar tokens.")),
  L("au-4-4", "O que a API valida", "cards", items=[
     dict(t="Assinatura", d=["O token foi emitido por quem tem a chave?", "Foi alterado?"]),
     dict(t="Emissor (iss)", d=["Foi emitido por quem esperamos?"]),
     dict(t="Audiência (aud)", d=["É um token para esta API?"]),
     dict(t="Validade (exp)", d=["Ainda não expirou?"]),
     dict(t="", d=["No ASP.NET Core, estas quatro verificações configuram-se no TokenValidationParameters.", "Se alguma falhar, a resposta é 401."], note=True)],
    more=dict(more="A audiência evita que um token emitido para a API A seja aceite pela API B. O ClockSkew é a tolerância entre relógios, por omissão cinco minutos; no AuthLab pomos zero para veres a expiração a acontecer à hora certa.", pit="Desligar ValidateIssuer, ValidateAudience ou ValidateLifetime para «fazer funcionar». O erro não desaparece: passa a ser uma falha de segurança.")),
  L("au-4-5", "O token não se revoga", "cards", items=[
     dict(t="O problema", d=["A API valida o token sozinha, sem perguntar a ninguém.", "Um token roubado funciona até expirar."]),
     dict(t="A resposta", d=["Access tokens curtos (minutos).", "Um refresh token para renovar, guardado no servidor e revogável."]),
     dict(t="", d=["Expiração curta e refresh token são as duas metades da mesma solução."], note=True)],
    more=dict(more="A vantagem do JWT (a API não precisa de ir à base de dados) é também a sua limitação (a API não sabe se o token foi revogado). Quando é mesmo preciso revogar já, mantém-se uma lista de tokens revogados e verifica-se em cada pedido, o que reintroduz a consulta que o JWT queria evitar.")),
 ],
 quiz=[
  Q("O que garante a assinatura de um JWT?", ["Que o conteúdo está encriptado", "Que o conteúdo não foi alterado", "Que o utilizador é maior de idade", "Que o token nunca expira"], 1, "A assinatura prova a integridade e a origem. Não esconde o conteúdo."),
  Q("Qual destas informações NÃO deve estar no payload?", ["O id do cliente", "O papel", "A password", "A hora de expiração"], 2, "O payload é legível por qualquer pessoa. Segredos nunca entram."),
  Q("Para que serve a claim aud?", ["Dizer para que API é o token", "Guardar a data de nascimento", "Identificar o utilizador", "Assinar o token"], 0, "A audiência impede que um token de uma API seja aceite por outra."),
  Q("Porque se usam access tokens de curta duração?", ["Para poupar memória", "Porque um token roubado deixa de servir quando expira", "Porque o JWT não aceita mais", "Para não precisar de HTTPS"], 1, "A API não consegue revogar o token, por isso a expiração curta limita o estrago."),
 ])

C5 = dict(id="auth-5", t="Hands-on I: gerar e validar um JWT", intro="Constróis de raiz uma Web API pequena, o AuthLab: configuras a autenticação JWT, crias no controller um método que gera o token e outro que só responde a quem o enviar. Não é a BankingApp: serve para perceberes cada peça antes do projeto.",
 lessons=[
  L("au-5-1", "Criar o projeto", "code", lang="sh", code=LAB_SH,
    points=["dotnet new webapi --use-controllers cria uma Web API com controllers.", "O pacote JwtBearer valida tokens.", "A chave tem de ter pelo menos 32 caracteres para HS256."],
    more=dict(more="Neste laboratório a chave fica no appsettings.json, para simplificar. Em produção, a mesma chave vem de uma variável de ambiente ou de um cofre (Azure Key Vault, por exemplo): o código lê sempre de builder.Configuration e não sabe a diferença.", pit="Copiar a chave do laboratório para um projeto real. Quem a tiver consegue fabricar tokens válidos.")),
  L("au-5-2", "Configuração", "code", lang="json", code=LAB_SETTINGS,
    points=["Issuer e Audience identificam quem emite e quem recebe o token.", "A chave (Jwt:Key) assina o token e tem pelo menos 32 caracteres.", "ExpiresMinutes controla a validade do token.", "Tudo fica na secção Jwt, lida pelo builder.Configuration."]),
  L("au-5-3", "Program.cs: configurar a autenticação", "code", lang="cs", code=LAB_PROGRAM,
    points=["A secção Jwt passa a um objeto JwtSettings, registado no container.", "AddJwtBearer configura as quatro validações.", "UseAuthentication e UseAuthorization na ordem certa.", "MapControllers expõe os controllers."],
    more=dict(more="O MapInboundClaims = false evita que o ASP.NET Core renomeie as claims do token (por exemplo, sub passaria a ser um nome comprido da Microsoft). Assim, o que vês no jwt.io é o que lês no código.\n\nRegistar o JwtSettings no container (AddSingleton) permite ao controller recebê-lo no construtor, tal como qualquer outro serviço. É a mesma Dependency Injection que já usaste.", pit="Trocar a ordem do UseAuthentication e do UseAuthorization. Todos os métodos protegidos passam a responder 401.")),
  L("au-5-4", "AuthController: gerar o token e usá-lo", "code", lang="cs", code=LAB_CONTROLLER,
    points=["Login é anónimo e gera o token, com as claims sub, name e role.", "Me tem [Authorize]: só responde com um token válido.", "A identidade vem do token: User.FindFirstValue(\"sub\").", "O Login devolve o mesmo 401 para email desconhecido e password errada."],
    more=dict(more="Este exemplo guarda as passwords em texto dentro da lista, só para o laboratório ser pequeno. A BankingApp guarda um hash (capítulo 7), e a criação do token vive numa classe própria (JwtTokenService), em vez de estar no controller.\n\nO [AllowAnonymous] no Login é explícito de propósito: quando mais tarde protegeres o controller inteiro com [Authorize], o Login continua a funcionar.", pit="Pôr [Authorize] no Login. Ninguém consegue obter o primeiro token.", tryit="Acrescenta uma claim email ao token e devolve-a no Me.")),
  L("au-5-5", "Bruno: o cabeçalho Authorization", "cards", items=BRUNO_LAB,
    more=dict(more="O Bruno guarda as coleções em ficheiros de texto (.bru), que podes pôr no repositório e rever em Pull Requests. A variável token é preenchida automaticamente a cada Login, por isso não copias o token à mão.", pit="Deixar o separador Auth em «No Auth» no pedido protegido. A API responde 401 e parece um erro do servidor.")),
  L("au-5-6", "Experimentar o AuthLab", "exercise",
    steps=[dict(lead="Arrancar", text="correr dotnet run e anotar o endereço https"),
           dict(lead="Sem token", text="GET /api/auth/me devolve 401"),
           dict(lead="Login", text="POST /api/auth/login com ana@example.com e Passw0rd! devolve o accessToken"),
           dict(lead="Com token", text="GET /api/auth/me com o Bearer Token devolve 200 com o id, nome e papel"),
           dict(lead="Descodificar", text="colar o token em jwt.io e identificar sub, name, role, iss, aud e exp"),
           dict(lead="Adulterar", text="alterar um carácter do token e confirmar que o Me responde 401"),
           dict(lead="Expirar", text="mudar ExpiresMinutes para 1, fazer login, esperar 61 segundos e confirmar o 401")],
    expected="GET  /api/auth/me (sem token)      -> 401\nPOST /api/auth/login               -> 200 { accessToken, expiresAtUtc }\nGET  /api/auth/me (com token)      -> 200 { id: \"1\", name: \"Ana Pereira\", role: \"Customer\" }\nGET  /api/auth/me (token alterado) -> 401\nGET  /api/auth/me (token expirado) -> 401",
    hint="Se o Me responde sempre 401, confirma a ordem do UseAuthentication e do UseAuthorization e se a chave do appsettings.json não mudou entre arranques.",
    extra="Troca o ClockSkew por 5 minutos e vê o token continuar válido depois de expirar.",
    more=dict(more="O passo «Adulterar» é o mais importante: mostra que a API não confia no conteúdo do token, confia na assinatura. Sem a chave, ninguém fabrica um token válido.", tryit="Troca uma letra no meio do payload (a segunda parte) e volta a chamar o Me.")),
 ],
 quiz=[
  Q("Onde fica a chave de assinatura durante o desenvolvimento?", ["Num cofre ou numa variável de ambiente", "No código-fonte", "No nome do projeto", "Num comentário"], 0, "Fora do repositório. Num laboratório pode ficar no appsettings.json, mas em produção vem de variáveis de ambiente ou de um cofre."),
  Q("O que devolve o método Me se o token tiver um carácter alterado?", ["200", "401", "403", "500"], 1, "A assinatura deixa de bater certo e a autenticação falha: 401."),
  Q("Porque tem o Login o atributo [AllowAnonymous]?", ["Para ser mais rápido", "Porque quem faz login ainda não tem token", "Porque o JWT o exige", "Para devolver 403"], 1, "O Login é o método que gera o primeiro token, por isso não pode exigir um."),
  Q("O que faz o atributo [Authorize] num método do controller?", ["Valida a password", "Exige um utilizador autenticado", "Emite o token", "Encripta a resposta"], 1, "Sem utilizador autenticado, a resposta é 401."),
 ])

C6 = dict(id="auth-6", t="Hands-on II: autorização", intro="Com o token a funcionar, decide-se o que cada utilizador pode fazer: papéis, políticas e dados que só pertencem ao dono. Continuas no AuthLab.",
 lessons=[
  L("au-6-1", "Papéis (roles)", "code", lang="cs", code=ROLE_CFG,
    points=["O token já leva a claim role.", "RoleClaimType diz ao ASP.NET Core qual claim é o papel.", "[Authorize(Roles = ...)] protege o método.", "Papel errado: 403."],
    more=dict(more="Sem RoleClaimType = \"role\", o ASP.NET Core procura a claim com o nome comprido da Microsoft e nunca encontra o papel: todos os pedidos dão 403, mesmo para o gestor.", pit="Papéis a mais. Quando os papéis passam de três ou quatro, reparas que estás a combinar regras: é a altura de usar policies.")),
  L("au-6-2", "Políticas (policies)", "code", lang="cs", code=POLICY,
    points=["Uma policy tem nome e agrupa regras.", "RequireRole e RequireClaim combinam-se.", "Reutiliza-se em vários métodos.", "Muda-se num sítio só."],
    more=dict(more="As policies também aceitam requisitos próprios (IAuthorizationRequirement e AuthorizationHandler), para regras que não são «tem esta claim», por exemplo «só entre as 9h e as 18h». Para as regras deste curso, RequireRole e RequireClaim chegam.")),
  L("au-6-3", "O recurso é teu?", "code", lang="cs", code=OWNER,
    points=["O id vem do token, nunca do pedido.", "Verifica que o recurso pertence ao utilizador.", "Se não pertence: 404, como se não existisse.", "Papéis e policies não chegam para isto."],
    more=dict(more="Papéis dizem «os clientes podem consultar contas». Não dizem «esta conta é tua». A verificação de propriedade faz-se no código, depois de carregar o recurso. É a falha de segurança mais frequente em APIs (a OWASP chama-lhe Broken Object Level Authorization): trocar o número na URL e ver a conta de outra pessoa.", pit="Receber o customerId no corpo ou na URL. Quem faz o pedido pode pôr lá qualquer valor.")),
  L("au-6-4", "Refresh token: renovar sem novo login", "code", lang="http", code=REFRESH_FLOW,
    points=["Access token curto, refresh token longo.", "O refresh token é aleatório e guardado no servidor (com hash).", "Cada renovação troca o refresh token por um novo (rotation).", "O logout apaga-o no servidor."],
    more=dict(more="Guardar o refresh token no servidor é o que permite revogar: apagas a linha e a sessão acaba. O access token continua válido até expirar, e é por isso que é curto.\n\nGuarda o refresh token com hash, tal como as passwords: se alguém ler a base de dados, não consegue usá-los.")),
  L("au-6-5", "Papéis e dados do dono no AuthLab", "exercise",
    steps=[dict(lead="Claims", text="configurar NameClaimType e RoleClaimType no TokenValidationParameters"),
           dict(lead="Gestores", text="criar o AdminController com GET /api/admin/customers só para o papel Manager"),
           dict(lead="Policy", text="criar a policy CanReviewLoans (papel Manager) e usá-la em POST /api/loans/{id}/approve"),
           dict(lead="Dono", text="criar uma lista de contas com CustomerId e GET /api/accounts/{number} que devolve 404 às contas de outros"),
           dict(lead="Testar", text="repetir os pedidos como ana (Customer) e como rui (Manager) e preencher a tabela de resultados")],
    table=[["Pedido", "Sem token", "Ana (Customer)", "Rui (Manager)"],
           ["GET /api/admin/customers", "401", "403", "200"],
           ["POST /api/loans/1/approve", "401", "403", "204"],
           ["GET /api/accounts/AC-001 (conta da Ana)", "401", "200", "404"],
           ["GET /api/accounts/AC-002 (conta do Rui)", "401", "404", "200"]],
    expected="Sem token -> 401 em todos\nCustomer num método de gestor -> 403\nConta de outro utilizador -> 404",
    extra="Acrescenta uma claim email_verified e uma policy VerifiedEmail.",
    more=dict(more="Se a tabela de resultados te sair diferente, é quase sempre uma de três causas: o RoleClaimType em falta (tudo 403), a ordem UseAuthentication/UseAuthorization (tudo 401) ou o id lido do sítio errado.")),
 ],
 quiz=[
  Q("Um Customer chama um método só para Manager. Que código recebe?", ["401", "403", "404", "200"], 1, "Está autenticado, mas o papel não chega: 403."),
  Q("De onde deve vir o id do cliente numa consulta às suas contas?", ["Do corpo do pedido", "Da URL", "Do token", "De um cabeçalho personalizado"], 2, "Do token assinado. Tudo o que vem no pedido pode ser forjado."),
  Q("Para que serve uma policy?", ["Guardar a password", "Agrupar regras de autorização com um nome reutilizável", "Emitir tokens", "Encriptar a ligação"], 1, "Combina papéis e claims numa regra com nome, usada em vários métodos."),
  Q("Porque se guarda o refresh token no servidor?", ["Para o poder revogar", "Para o tornar mais curto", "Porque o JWT o exige", "Para poupar espaço"], 0, "Apagar o refresh token termina a sessão. Um access token não se consegue revogar."),
 ])

C7 = dict(id="auth-7", t="Segurança na prática", intro="O que separa um exemplo que funciona de uma API que se pode pôr em produção: passwords, segredos, HTTPS e os erros comuns.",
 lessons=[
  L("au-7-1", "Passwords: hash, nunca encriptação", "code", lang="cs", code=HASH,
    points=["Guarda-se o hash, nunca a password.", "O hash tem sal aleatório: o mesmo texto dá hashes diferentes.", "Verifica-se com VerifyHashedPassword.", "O hash é lento de propósito."],
    more=dict(more="Encriptar é reversível: quem tiver a chave recupera a password. O hash não tem volta; o login compara o hash da password escrita com o hash guardado. O sal evita que duas pessoas com a mesma password tenham o mesmo hash e inutiliza as tabelas de hashes pré-calculados.\n\nO PasswordHasher de ASP.NET Core Identity já faz isto bem (PBKDF2 com sal e muitas iterações). Não inventes o teu algoritmo.", pit="Guardar um hash simples (SHA256 ou MD5) de uma password. São rápidos, e um atacante testa milhares de milhões de palpites por segundo.")),
  L("au-7-2", "Checklist de uma API protegida", "cards", items=[
     dict(t="Transporte", check=True, d=["HTTPS sempre, com redirecionamento", "O token só no cabeçalho Authorization, nunca no URL"]),
     dict(t="Segredos", check=True, d=["Chave do JWT em variáveis de ambiente ou num cofre", "Nenhum segredo em ficheiros do Git"]),
     dict(t="Tokens", check=True, d=["Access token curto (minutos)", "Validar emissor, audiência, validade e assinatura", "Poucas claims, nenhum segredo"]),
     dict(t="Passwords", check=True, d=["Só o hash, com PasswordHasher", "Mínimo de 8 caracteres", "Mesma resposta para email desconhecido e password errada"]),
     dict(t="Autorização", check=True, d=["Todos os endpoints protegidos por omissão", "Id do utilizador sempre do token", "404 para recursos de outros utilizadores"]),
     dict(t="Operação", check=True, d=["Não registar passwords nem tokens", "Limitar tentativas de login", "Mensagens de erro sem detalhes internos"])],
    more=dict(more="Uma boa prática é inverter a lógica: protege tudo e abre só o que é público. No ASP.NET Core faz-se com uma FallbackPolicy que exige utilizador autenticado, e [AllowAnonymous] nos endpoints públicos. Assim, um endpoint novo esquecido fica protegido e não aberto.")),
  L("au-7-3", "Onde guardar o token no cliente", "table", rows=[
     ["Local", "Risco", "Nota"],
     ["localStorage", "Qualquer script na página lê o token (XSS)", "Simples, mas exposto."],
     ["Cookie HttpOnly + Secure + SameSite", "Scripts não conseguem lê-lo", "Exige proteção contra CSRF."],
     ["Memória da aplicação", "Perde-se ao recarregar", "Mais seguro, com refresh token para recuperar."],
     ["Cofre do sistema (apps móveis)", "Protegido pelo sistema operativo", "Keychain no iOS, Keystore no Android."]],
    more=dict(more="Não há uma resposta única. Cada opção troca um risco por outro. O importante é saberes qual escolheste e porquê. Este tema pertence ao cliente (web ou móvel), mas quem desenha a API precisa de o conhecer, porque define como o token é enviado.")),
  L("au-7-4", "Rever o AuthLab com olhos de atacante", "exercise",
    steps=[dict(lead="Hash", text="substituir as passwords em texto por hashes com PasswordHasher"),
           dict(lead="Por omissão", text="exigir autenticação em todos os endpoints com uma FallbackPolicy e abrir o Login e os endpoints públicos com AllowAnonymous"),
           dict(lead="Limite", text="bloquear o login durante 1 minuto após 5 tentativas falhadas do mesmo email"),
           dict(lead="Logs", text="confirmar que nenhum log escreve a password nem o token"),
           dict(lead="Explicar", text="escrever três frases sobre o que acontece se alguém roubar o access token e o que limita o estrago")],
    expected="Tentativa 6 do mesmo email -> 429 Too Many Requests (ou 401 com mensagem genérica)\nEndpoint novo sem atributo -> 401",
    extra="Acrescenta um endpoint /refresh com rotation, como no capítulo anterior.",
    more=dict(more="Rever com olhos de atacante é perguntar: se eu fosse mal-intencionado, o que tentava? Trocar o id na URL, repetir uma password mil vezes, reutilizar um token expirado, ler o payload à procura de segredos. A checklist do início do capítulo responde às mesmas perguntas."))
 ],
 quiz=[
  Q("O que se guarda na base de dados em vez da password?", ["A password encriptada", "O hash com sal", "A password em base64", "Nada"], 1, "O hash é irreversível e o sal evita hashes iguais para passwords iguais."),
  Q("Onde NÃO deve ir o token de acesso num pedido?", ["No cabeçalho Authorization", "No URL", "Num cookie HttpOnly", "Na memória do cliente"], 1, "URLs ficam em logs, histórico e referers."),
  Q("O que faz uma FallbackPolicy que exige autenticação?", ["Abre todos os endpoints", "Protege por omissão os endpoints sem atributo", "Gera tokens", "Desliga o HTTPS"], 1, "Um endpoint novo esquecido fica protegido, e não aberto."),
  Q("Porque se limitam as tentativas de login?", ["Para poupar CPU", "Para travar ataques de adivinhação de passwords", "Porque o JWT o exige", "Para expirar o token"], 1, "Sem limite, um atacante testa passwords à vontade."),
 ])

MOD_AUTH = dict(
 id="auth", num=4, kind="course", title="Autenticação e Autorização", short="Autenticação",
 tagline="A diferença entre Basic Auth e OAuth 2.0, como funciona um JWT e um hands-on onde emites, validas e proteges com tokens.",
 chapters=[C1, C2, C3, C4, C5, C6, C7],
 outro=dict(
  done=["Distinguir autenticação de autorização e escolher entre 401, 403 e 404",
        "Explicar as diferenças entre Basic Auth e OAuth 2.0",
        "Identificar os papéis e os fluxos do OAuth 2.0",
        "Ler um JWT e perceber o que a API valida",
        "Emitir e validar um JWT em ASP.NET Core",
        "Proteger endpoints com papéis, policies e verificação de propriedade"],
  docs=[dict(t="Autenticação e autorização no ASP.NET Core", u="https://learn.microsoft.com/aspnet/core/security/"),
        dict(t="Autenticação JWT Bearer", u="https://learn.microsoft.com/aspnet/core/security/authentication/"),
        dict(t="OAuth 2.0 e OpenID Connect", u="https://oauth.net/2/"),
        dict(t="Bruno", u="https://www.usebruno.com/")],
  practice=["Acrescentar um endpoint /refresh ao AuthLab", "Criar uma policy com um requisito próprio", "Mudar a assinatura de HS256 para RS256", "Ler o OWASP API Security Top 10"]))
