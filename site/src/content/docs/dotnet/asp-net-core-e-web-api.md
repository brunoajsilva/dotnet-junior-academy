---
title: "ASP.NET Core e Web API"
description: "Construir uma Web API: pipeline, controllers, códigos HTTP, DTOs, validação e documentação."
sidebar:
  order: 2
---

Construir uma Web API: pipeline, controllers, códigos HTTP, DTOs, validação e documentação.

## Program.cs: arrancar a aplicação

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();

var app = builder.Build();

app.MapOpenApi();
app.UseHttpsRedirection();
app.MapControllers();

app.Run();
```

- builder regista serviços.
- app define como os pedidos são tratados.
- Run arranca o servidor Kestrel.
- Tudo num só ficheiro, de cima para baixo.

<details>
<summary>Saber mais</summary>

O Program.cs tem duas fases. Primeiro o builder regista os serviços de que a aplicação precisa (controllers, OpenAPI, base de dados). Depois, com app = builder.Build(), configuras o pipeline: o que acontece a cada pedido, pela ordem em que escreves.

O servidor web por baixo chama-se Kestrel e arranca com app.Run().

</details>

## Middleware: o pipeline de pedidos

1. **Pedido** HTTP
2. **HTTPS** redireciona para https
3. **Autenticação** quem és?
4. **Autorização** podes fazer isto?
5. **Controller** executa a ação

:::note[Nota]
Cada middleware pode tratar o pedido, passá-lo ao seguinte ou terminá-lo.

A ordem do registo no Program.cs é a ordem de execução.

A resposta volta pelo mesmo caminho, em sentido contrário.
:::

<details>
<summary>Saber mais</summary>

O pipeline é uma cadeia: cada middleware pode responder logo (por exemplo, rejeitar um pedido sem autenticação) ou passar ao seguinte. Quando o controller devolve a resposta, esta volta pela mesma cadeia, ao contrário. É por isso que a ordem no Program.cs importa.

</details>

## Middleware próprio

```csharp
app.Use(async (context, next) =>
{
    var sw = Stopwatch.StartNew();

    await next();

    var ms = sw.ElapsedMilliseconds;
    Console.WriteLine($"{context.Request.Path}: {ms} ms");
});
```

- Use acrescenta um middleware ao pipeline.
- O código antes de next() corre à ida.
- O código depois corre à volta.
- Serve para logging, medição de tempos e tratamento de erros.

<details>
<summary>Saber mais</summary>

Um middleware é um passo do pipeline. Recebe o contexto do pedido e uma função next. O código antes de await next() corre à ida; o código depois corre à volta, já com a resposta construída.

É o sítio certo para preocupações transversais: medir tempos, registar pedidos, converter exceções em respostas HTTP.

:::caution[Armadilha]
Registar o middleware de erros depois dos controllers. A ordem do registo é a ordem de execução.
:::

</details>

## Configuração e ambientes

```csharp
// appsettings.json
{
  "ConnectionStrings": {
    "BankingApp": "Server=...;Database=BankingApp"
  },
  "Interest": { "MaxBonus": 0.02 }
}

// in code
var cs = builder.Configuration
    .GetConnectionString("BankingApp");
var max = builder.Configuration
    .GetValue<decimal>("Interest:MaxBonus");
```

- appsettings.json guarda a configuração.
- O ficheiro do ambiente sobrepõe-se ao base.
- Variáveis de ambiente têm prioridade.
- Segredos nunca vão para o repositório.

<details>
<summary>Saber mais</summary>

A configuração vem de várias fontes sobrepostas: appsettings.json, appsettings.\{Environment\}.json, variáveis de ambiente. A última a ser lida ganha. Assim o mesmo código usa uma base de dados em DEV e outra em PROD, sem recompilar.

Segredos (passwords, chaves) nunca vão para o repositório; usam-se variáveis de ambiente, user-secrets em desenvolvimento ou um cofre.

</details>

## Controllers e rotas

```csharp
[ApiController]
[Route("api/accounts")]
public class AccountsController : ControllerBase
{
    [HttpGet]                     // GET api/accounts
    public IActionResult List() { ... }

    [HttpGet("{number}")]         // GET api/accounts/AC-001
    public IActionResult Get(string number) { ... }

    [HttpPost]                    // POST api/accounts
    public IActionResult Create(NewAccount r) { ... }
}
```

- \[ApiController\] liga o binding e a validação automática.
- \[Route\] define o caminho base.
- Um atributo por verbo: HttpGet, HttpPost...
- \{number\} vem da rota; o corpo vem do JSON.

<details>
<summary>Saber mais</summary>

Um controller é uma classe que agrupa endpoints. \[ApiController\] ativa o binding automático e a validação; \[Route\] define o caminho base; cada método tem um atributo de verbo. Parâmetros como \{number\} vêm da rota, e o corpo JSON é convertido para o tipo do parâmetro.

</details>

## Códigos de estado HTTP

| Código | Significado | Quando |
| --- | --- | --- |
| 200 OK | Pedido bem-sucedido, com corpo | GET que encontra o recurso |
| 201 Created | Recurso criado (cabeçalho Location) | POST que cria uma conta |
| 204 No Content | Sucesso, sem corpo | DELETE ou PUT bem-sucedidos |
| 400 Bad Request | Pedido inválido | Falha na validação |
| 404 Not Found | O recurso não existe | GET de uma conta inexistente |
| 409 Conflict | Conflito com o estado atual | Número de conta repetido |
| 500 Internal Server Error | Erro no servidor | Exceção não tratada |

<details>
<summary>Saber mais</summary>

Os códigos agrupam-se por centena: 2xx sucesso, 4xx erro do cliente (corrige o pedido), 5xx erro do servidor (a culpa não é do cliente). Escolher o código certo poupa horas de depuração a quem consome a tua API.

:::tip[Experimenta]
Antes de abrires a coluna «Quando», tenta adivinhar o código para cada situação.
:::

</details>

## Devolver o resultado certo

```csharp
[HttpGet("{number}")]
public ActionResult<AccountResponse> Get(string number)
{
    var account = _service.Get(number);
    if (account is null)
        return NotFound();

    return Ok(account);
}

[HttpPost]
public ActionResult<AccountResponse> Create(NewAccount r)
{
    var created = _service.Create(r);
    return CreatedAtAction(nameof(Get),
        new { number = created.Number }, created);
}
```

- Ok, NotFound, BadRequest...
- CreatedAtAction devolve 201 e o endereço do novo recurso.
- ActionResult\<T\> documenta o tipo devolvido.

<details>
<summary>Saber mais</summary>

O código de estado é parte do contrato da API. Os métodos auxiliares (Ok, NotFound, BadRequest, CreatedAtAction) devolvem o código certo. ActionResult\<T\> permite devolver tanto o objeto como um código de erro, e o OpenAPI percebe o tipo.

:::tip[Experimenta]
Faz GET de uma conta que não existe e confirma que recebes 404 e não 200 com corpo vazio.
:::

</details>

## DTOs e validação

```csharp
public record NewAccount(
    [Required, StringLength(20)] string Number,
    [RegularExpression(@"^\d{9}$")] string TaxId,
    [Range(0, 1000000)] decimal Balance);

public record AccountResponse(
    string Number, string Customer, decimal Balance);
```

- DTO é o formato do pedido ou da resposta, não da base de dados.
- Entrada e saída ficam separadas.
- Os atributos validam o pedido.
- Com \[ApiController\], um pedido inválido devolve 400 sozinho.

<details>
<summary>Saber mais</summary>

Um DTO descreve o formato do pedido ou da resposta, e não o da tabela. Separar entrada de saída (NewAccount vs AccountResponse) permite alterar a base de dados sem partir os clientes da API, e impede que o cliente defina campos que não deve (como o Id).

Os atributos de validação (\[Required\], \[Range\], \[StringLength\]) são verificados antes de o controller correr; com \[ApiController\], um pedido inválido devolve 400 sozinho.

:::caution[Armadilha]
Devolver a entidade da base de dados diretamente. Qualquer alteração à tabela passa a alterar o contrato público.
:::

</details>

## REST e RPC

#### REST

- Recursos e verbos HTTP
- O URL identifica o recurso; o verbo diz o que fazer.

```csharp
GET    /api/accounts/AC-001
POST   /api/accounts
DELETE /api/accounts/AC-001
```

#### RPC

- Operações com nome
- O URL identifica a operação; quase tudo é POST.

```csharp
POST /api/calculateInterest
POST /api/closeAccount
POST /api/sendEmail
```

<details>
<summary>Saber mais</summary>

Numa API REST, o URL é um substantivo (o recurso) e o verbo HTTP é a ação: GET lê, POST cria, PUT/PATCH altera, DELETE apaga. Em RPC, o URL é um verbo (calculateInterest) e quase tudo é POST. REST é a escolha por omissão para os recursos do domínio; RPC aparece em operações que não são um recurso, como «calcular».

</details>

## Documentar com OpenAPI e Swagger UI

```csharp
// 1. the document: built into ASP.NET Core (the template already has it)
builder.Services.AddOpenApi();

// 2. the UI: a separate package
// dotnet add package Swashbuckle.AspNetCore.SwaggerUI

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();   // serves /openapi/v1.json
    app.UseSwaggerUI(o =>
        o.SwaggerEndpoint("/openapi/v1.json", "v1"));   // /swagger
}
```

- OpenAPI é o documento que descreve o contrato da API: endpoints, parâmetros e respostas.
- Desde o .NET 9, o ASP.NET Core gera esse documento sozinho (Microsoft.AspNetCore.OpenApi).
- O template deixou de incluir o Swashbuckle e, no .NET 10, o documento é OpenAPI 3.1.
- A página para experimentar é uma peça à parte: o pacote Swashbuckle.AspNetCore.SwaggerUI.

<details>
<summary>Saber mais</summary>

São duas peças diferentes. O documento OpenAPI (o JSON em /openapi/v1.json) é gerado pelo próprio ASP.NET Core com AddOpenApi e MapOpenApi. A página interativa (o Swagger UI) só desenha esse documento: não o gera.

Antes do .NET 9, o template incluía o Swashbuckle, que fazia as duas coisas. Agora o documento é nativo e, se quiseres a página do Swagger UI, acrescentas o pacote Swashbuckle.AspNetCore.SwaggerUI e apontas-o para o documento. Existem outras interfaces que leem o mesmo documento (Scalar, ReDoc), por isso trocar de UI não mexe na API.

O .NET 10 passou o documento para OpenAPI 3.1 por omissão. Se algum cliente ou ferramenta não o suportar, podes fixar a versão 3.0 nas opções do AddOpenApi.

:::caution[Armadilha]
Abrir /swagger e receber 404. Sem o pacote SwaggerUI, ou fora do ambiente Development, a página não existe, mas o documento /openapi/v1.json continua a funcionar.
:::

:::tip[Experimenta]
Abre primeiro /openapi/v1.json e depois /swagger. Executa um POST e vê o 201 com o cabeçalho Location.
:::

</details>

## API de contas

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Controller.** AccountsController com uma lista de contas em memória
2. **Listar.** GET /api/accounts devolve todas as contas
3. **Obter.** GET /api/accounts/\{number\} devolve 404 se não existir
4. **Criar.** POST /api/accounts valida o pedido (400) e rejeita números repetidos (409)
5. **Experimentar.** testar todos os casos no Swagger UI

| Pedido | Sucesso | Erros |
| --- | --- | --- |
| GET /api/accounts | 200 com a lista | — |
| GET /api/accounts/\{number\} | 200 com a conta | 404 se não existir |
| POST /api/accounts | 201 com Location | 400 se inválido; 409 se repetida |

:::note[Extra]
Acrescentar DELETE /api/accounts/\{number\}, que devolve 204 ou 404.
:::

<details>
<summary>Saber mais</summary>

Só passas ao capítulo seguinte quando o resultado esperado aparecer no teu computador. Se algo falhar, lê a mensagem de erro de baixo para cima: a última linha costuma dizer o que correu mal.

:::tip[Experimenta]
Acrescentar DELETE /api/accounts/\{number\}, que devolve 204 ou 404.
:::

</details>

## Quiz

Responde de cabeça antes de abrires cada resposta.

### Pergunta 1

Que código HTTP devolve um POST que criou uma conta?

- **A.** 200 OK
- **B.** 201 Created
- **C.** 204 No Content
- **D.** 202 Accepted

<details>
<summary>Ver resposta</summary>

**B. 201 Created**

201 Created, com o cabeçalho Location do novo recurso.

</details>

### Pergunta 2

O que acontece à ordem dos middlewares no Program.cs?

- **A.** É irrelevante
- **B.** É a ordem de execução do pipeline
- **C.** Corre ao contrário
- **D.** O framework reordena-os

<details>
<summary>Ver resposta</summary>

**B. É a ordem de execução do pipeline**

Cada middleware corre pela ordem do registo; a resposta volta em sentido contrário.

</details>

### Pergunta 3

Porque se usam DTOs em vez de devolver a entidade?

- **A.** Por exigência do EF Core
- **B.** Para separar o contrato da API do modelo da base de dados
- **C.** Para o JSON ficar mais pequeno
- **D.** Porque as entidades não são serializáveis

<details>
<summary>Ver resposta</summary>

**B. Para separar o contrato da API do modelo da base de dados**

Assim a base de dados pode mudar sem partir os clientes da API.

</details>

### Pergunta 4

Qual o código para uma conta com número repetido?

- **A.** 400
- **B.** 404
- **C.** 409
- **D.** 500

<details>
<summary>Ver resposta</summary>

**C. 409**

409 Conflict: o pedido conflita com o estado atual.

</details>
