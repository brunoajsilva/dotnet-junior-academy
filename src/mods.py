# -*- coding: utf-8 -*-
# Module 1 (academy intro) and Module 4 (final project): handwritten content.

MOD1 = dict(
 id="academia", num=1, kind="intro", title="Introdução à Academia", short="Academia",
 tagline="O que é a .NET Backend Academy, o que vais conseguir fazer no fim, como está organizada e o que tens de instalar.",
 sections=[
  dict(id="what", title="O que é", blocks=[
   dict(k="p", t="A .NET Backend Academy é o programa de integração técnica para quem chega à equipa de backend. Em vez de leres teoria durante semanas, escreves código desde o primeiro dia, num domínio que conheces do trabalho real: uma seguradora, com clientes, apólices e prémios."),
   dict(k="p", t="Começas por C#, passas para a plataforma .NET e terminas com uma API completa, construída de raiz com Clean Architecture. Cada módulo usa o que aprendeste no anterior, por isso nada fica a flutuar."),
   dict(k="cards", items=[
    dict(t="Prática primeiro", d="Cada tema tem uma explicação curta e um exercício. A maior parte do tempo estás a escrever código.",
         more=dict(more="Os exemplos são pequenos de propósito: cabem num ecrã e podes correr tudo no teu computador. Quando um tema tem mais profundidade, encontras um botão «Saber mais» com a explicação completa, os erros mais comuns e uma experiência para fazeres.", tryit="Abre o primeiro tema de C# e carrega em «Saber mais» para veres como funciona.")),
    dict(t="Um domínio só", d="Clientes, apólices e prémios aparecem em todos os módulos, do primeiro exercício ao projeto final.",
         more=dict(more="Usar sempre o mesmo domínio tira-te o esforço de perceber um problema novo em cada exercício. O foco fica na tecnologia: como se modela um Customer em C#, como se guarda com o EF Core, como se expõe numa API, como se testa.")),
    dict(t="Explicar o que fizeste", d="No fim de cada bloco explicas o teu código e respondes a perguntas de «porquê».",
         more=dict(more="Saber escrever código é metade do trabalho. A outra metade é explicá-lo a um colega numa revisão. As perguntas de «porquê» (por exemplo, porque usámos decimal e não double?) treinam essa segunda metade."))
   ]),
  ]),
  dict(id="goals", title="Objetivos", blocks=[
   dict(k="p", t="No fim da Academia consegues ler, alterar e criar código backend em .NET dentro da equipa. Cada módulo acrescenta uma capacidade concreta."),
   dict(k="outcomes", items=[
    dict(mod="csharp", t="Ler e escrever C#", d="Tipos, decisões, ciclos, strings e métodos. Modelar um domínio com classes, records e interfaces. Consultar com LINQ, tratar erros e usar async/await.",
         more=dict(more="Resultado verificável: uma aplicação de consola completa, feita a partir de um enunciado, que regista apólices e calcula totais por cliente.")),
    dict(mod="dotnet", t="Construir e organizar uma API", d="Como o .NET executa o código, ASP.NET Core, Dependency Injection, Entity Framework Core, testes e camadas.",
         more=dict(more="Resultado verificável: uma Web API que guarda apólices numa base de dados SQL Server, com testes unitários a passar e o código organizado em camadas.")),
    dict(mod="projeto", t="Juntar tudo num projeto real", d="Uma API de apólices com Clean Architecture, construída de raiz sem projeto de partida.",
         more=dict(more="Resultado verificável: uma solução com cinco projetos, migrations, endpoints documentados, tratamento de erros por middleware e testes aos handlers."))
   ]),
  ]),
  dict(id="plan", title="Plano", blocks=[
   dict(k="p", t="Quatro módulos, por esta ordem. Carrega num capítulo para saltar diretamente para ele."),
   dict(k="plan"),
  ]),
  dict(id="how", title="Como funciona", blocks=[
   dict(k="p", t="Cada tema segue o mesmo ritmo: ouvir, experimentar e explicar."),
   dict(k="steps", items=[
    dict(t="Aprender", d="Explicação curta com um exemplo real e leitura guiada da documentação oficial.",
         more=dict(more="Neste site é o cartão do tema: pontos-chave e um exemplo de código. Se quiseres ir mais fundo, abre o «Saber mais».")),
    dict(t="Fazer", d="Exercício prático em que escreves o código, com apoio nas partes mais difíceis.",
         more=dict(more="Os exercícios têm uma lista de passos que podes ir marcando, o resultado esperado (para saberes que chegaste ao fim) e um extra opcional para quem acaba cedo.")),
    dict(t="Explicar", d="Demonstras o que fizeste e respondes a perguntas de «porquê».",
         more=dict(more="Não é um exame. É uma conversa de equipa: mostras o código, explicas as decisões e dizes o que farias diferente."))
   ]),
   dict(k="cards", title="Como tirar partido deste site", items=[
    dict(t="Saber mais", d="Os botões com este nome abrem um painel com a explicação completa, sem sair do tema.", more=dict(more="O painel fecha com Esc ou ao clicares fora dele. Podes abri-lo em qualquer tema, por qualquer ordem.")),
    dict(t="Pesquisar", d="Carrega em / ou Ctrl+K para procurar um tema em todos os módulos.", more=dict(more="A pesquisa encontra palavras dos títulos e dos pontos-chave. Prime Enter para abrir o primeiro resultado.")),
    dict(t="Progresso", d="Marca os temas como vistos. O progresso fica guardado neste browser.", more=dict(more="O progresso é guardado apenas neste computador e neste browser. Se limpares os dados do browser, perde-se."))
   ]),
  ]),
  dict(id="software", title="Software necessário", blocks=[
   dict(k="p", t="Instala e verifica estes componentes antes de começares o módulo de C#. Marca cada um quando o comando de verificação der o resultado esperado."),
   dict(k="software", items=[
    dict(id="sdk", need="req", name=".NET SDK 10", why="Compilador, comando dotnet e templates de projeto.",
         check="dotnet --version", expect="10.0.x", install="Instalador do SDK em dotnet.microsoft.com/download (escolhe o .NET 10, versão LTS).",
         more=dict(more="O SDK inclui o runtime, por isso não precisas de instalar mais nada para executar as aplicações. Se tiveres várias versões, dotnet --list-sdks mostra todas.")),
    dict(id="ide", need="req", name="IDE: Visual Studio, VS Code ou Rider", why="Editor com depuração, IntelliSense e gestão de pacotes.",
         check="", expect="Abre uma consola .NET e corre-a com F5.", install="Visual Studio 2026 com a carga de trabalho «ASP.NET and web development», ou VS Code com a extensão C# Dev Kit, ou JetBrains Rider.",
         more=dict(more="Usa o IDE que a equipa aprovou. Os exercícios são feitos com a linha de comandos (dotnet new, dotnet build, dotnet run), por isso funcionam com qualquer um. O Visual Studio é o mais completo no Windows; o VS Code funciona em qualquer sistema.")),
    dict(id="git", need="req", name="Git", why="Controlo de versões. Todo o código do curso vive num repositório.",
         check="git --version", expect="git version 2.x", install="git-scm.com/downloads.",
         more=dict(more="Depois de instalar, configura o teu nome e e-mail:\n\ngit config --global user.name \"O Teu Nome\"\ngit config --global user.email \"nome@empresa.pt\"")),
    dict(id="sql", need="req", name="SQL Server", why="Base de dados dos módulos de Entity Framework Core e do projeto final.",
         check="sqlcmd -S localhost -Q \"SELECT @@VERSION\"", expect="Microsoft SQL Server 20xx ...", install="SQL Server Developer ou LocalDB (instalado com o Visual Studio), ou um container Docker com a imagem do SQL Server.",
         more=dict(more="Para os exercícios, o LocalDB chega e não precisa de configuração. A connection string típica é Server=(localdb)\\MSSQLLocalDB;Database=Insurance;Trusted_Connection=True;TrustServerCertificate=True. Se usares Docker, a porta e a password são as que definires no container.")),
    dict(id="sqlclient", need="req", name="Cliente SQL", why="Ver as tabelas e os dados que o EF Core cria.",
         check="", expect="Consegues ligar-te ao servidor e listar as bases de dados.", install="SQL Server Management Studio, Azure Data Studio ou a extensão SQL do VS Code.",
         more=dict(more="Vais usá-lo para confirmar que a migration criou as tabelas e que o POST gravou uma linha.")),
    dict(id="ef", need="req", name="Ferramenta dotnet-ef", why="Comandos para criar e aplicar migrations.",
         check="dotnet ef --version", expect="Entity Framework Core .NET Command-line Tools 10.x", install="dotnet tool install --global dotnet-ef",
         more=dict(more="É uma ferramenta global do .NET, instalada uma única vez por computador. Para atualizar: dotnet tool update --global dotnet-ef.")),
    dict(id="api", need="req", name="Postman ou Bruno", why="Enviar pedidos HTTP à tua API e guardá-los numa coleção.",
         check="", expect="Consegues enviar um GET a qualquer URL público.", install="postman.com ou usebruno.com.",
         more=dict(more="O Bruno guarda as coleções em ficheiros de texto, o que facilita pô-las no repositório. O Postman tem mais integrações. Ambos importam o documento OpenAPI da tua API.")),
    dict(id="docker", need="opt", name="Docker Desktop", why="Alternativa para correr o SQL Server num container.",
         check="docker --version", expect="Docker version 2x", install="docker.com/products/docker-desktop.",
         more=dict(more="Só é necessário se não usares o LocalDB. Confirma com a equipa se o licenciamento do Docker Desktop está coberto pela empresa.")),
    dict(id="stack", need="later", name="SingleStore, Redis e Kafka", why="Fazem parte da stack dos projetos da equipa.",
         check="", expect="", install="Não precisas de os instalar agora.",
         more=dict(more="Estas tecnologias são usadas nos projetos reais, mas não entram nos exercícios da Academia. Serão apresentadas depois de a terminares."))
   ]),
  ]),
 ])

# ------------------------------------------------------------------ MODULE 4
CS = {}
CS["domain"] = r'''namespace Insurance.Domain;

public class InvalidPolicyException : Exception
{
    public InvalidPolicyException(string message) : base(message) { }
}

public class Customer
{
    private Customer() { }   // required by EF Core

    public Customer(string name, string taxId)
    {
        if (taxId.Length != 9 || !taxId.All(char.IsDigit))
            throw new InvalidPolicyException($"Invalid tax id: {taxId}");

        Name = name;
        TaxId = taxId;
    }

    public int Id { get; private set; }
    public string Name { get; private set; } = "";
    public string TaxId { get; private set; } = "";
    public List<Policy> Policies { get; private set; } = [];
}

public enum PolicyStatus { Active, Cancelled }

public class Policy
{
    private Policy() { }   // required by EF Core

    public static Policy Create(string number, Customer customer, decimal premium, DateOnly start)
    {
        if (string.IsNullOrWhiteSpace(number))
            throw new InvalidPolicyException("Number is required.");
        if (premium <= 0)
            throw new InvalidPolicyException("Premium must be positive.");

        return new Policy
        {
            Number = number,
            Customer = customer,
            Premium = premium,
            Start = start,
            Status = PolicyStatus.Active
        };
    }

    public int Id { get; private set; }
    public string Number { get; private set; } = "";
    public int CustomerId { get; private set; }
    public Customer Customer { get; private set; } = null!;
    public decimal Premium { get; private set; }
    public DateOnly Start { get; private set; }
    public PolicyStatus Status { get; private set; }

    public void Cancel()
    {
        if (Status == PolicyStatus.Cancelled)
            throw new InvalidPolicyException($"Policy {Number} is already cancelled.");

        Status = PolicyStatus.Cancelled;
    }
}'''
CS["calc"] = r'''namespace Insurance.Domain;

public interface IPremiumCalculator
{
    decimal Calculate(decimal basePremium, int existingPolicies);
}

public class DiscountedPremium : IPremiumCalculator
{
    public decimal Calculate(decimal basePremium, int existingPolicies)
        => existingPolicies > 0
            ? Math.Round(basePremium * 0.90m, 2)   // 10% off for returning customers
            : basePremium;
}'''
CS["abstr"] = r'''using Insurance.Domain;

namespace Insurance.Application.Abstractions;

public interface IPolicyRepository
{
    Task<Policy?> GetByNumberAsync(string number, CancellationToken ct);
    Task<bool> ExistsAsync(string number, CancellationToken ct);
    Task<IReadOnlyList<Policy>> ListAsync(CancellationToken ct);
    Task AddAsync(Policy policy, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}

public interface ICustomerRepository
{
    Task<Customer?> GetByTaxIdAsync(string taxId, CancellationToken ct);
}'''
CS["create"] = r'''using Insurance.Application.Abstractions;
using Insurance.Domain;

namespace Insurance.Application.Policies;

// 1. The command: only data
public record CreatePolicyCommand(string Number, string CustomerName, string TaxId, decimal BasePremium);

// 2. What the use case returns
public record PolicyResult(string Number, string CustomerName, decimal Premium, DateOnly Start, string Status)
{
    public static PolicyResult From(Policy p)
        => new(p.Number, p.Customer.Name, p.Premium, p.Start, p.Status.ToString());
}

public class PolicyAlreadyExistsException : Exception
{
    public PolicyAlreadyExistsException(string number)
        : base($"Policy {number} already exists.") { }
}

// 3. The handler: the business rules of this use case
public class CreatePolicyHandler
{
    private readonly IPolicyRepository _policies;
    private readonly ICustomerRepository _customers;
    private readonly IPremiumCalculator _calculator;

    public CreatePolicyHandler(
        IPolicyRepository policies,
        ICustomerRepository customers,
        IPremiumCalculator calculator)
    {
        _policies = policies;
        _customers = customers;
        _calculator = calculator;
    }

    public async Task<PolicyResult> HandleAsync(CreatePolicyCommand command, CancellationToken ct)
    {
        if (await _policies.ExistsAsync(command.Number, ct))
            throw new PolicyAlreadyExistsException(command.Number);

        var customer = await _customers.GetByTaxIdAsync(command.TaxId, ct)
                       ?? new Customer(command.CustomerName, command.TaxId);

        var premium = _calculator.Calculate(command.BasePremium, customer.Policies.Count);
        var policy = Policy.Create(command.Number, customer, premium, DateOnly.FromDateTime(DateTime.Today));

        await _policies.AddAsync(policy, ct);
        await _policies.SaveChangesAsync(ct);

        return PolicyResult.From(policy);
    }
}'''
CS["queries"] = r'''using Insurance.Application.Abstractions;

namespace Insurance.Application.Policies;

public class PolicyNotFoundException : Exception
{
    public PolicyNotFoundException(string number)
        : base($"Policy {number} was not found.") { }
}

public record GetPolicyQuery(string Number);

public class GetPolicyHandler
{
    private readonly IPolicyRepository _policies;

    public GetPolicyHandler(IPolicyRepository policies) => _policies = policies;

    public async Task<PolicyResult> HandleAsync(GetPolicyQuery query, CancellationToken ct)
    {
        var policy = await _policies.GetByNumberAsync(query.Number, ct)
                     ?? throw new PolicyNotFoundException(query.Number);

        return PolicyResult.From(policy);
    }
}

public record CancelPolicyCommand(string Number);

public class CancelPolicyHandler
{
    private readonly IPolicyRepository _policies;

    public CancelPolicyHandler(IPolicyRepository policies) => _policies = policies;

    public async Task HandleAsync(CancelPolicyCommand command, CancellationToken ct)
    {
        var policy = await _policies.GetByNumberAsync(command.Number, ct)
                     ?? throw new PolicyNotFoundException(command.Number);

        policy.Cancel();                       // the rule lives in the Domain
        await _policies.SaveChangesAsync(ct);
    }
}

public record ListPoliciesQuery;

public class ListPoliciesHandler
{
    private readonly IPolicyRepository _policies;

    public ListPoliciesHandler(IPolicyRepository policies) => _policies = policies;

    public async Task<IReadOnlyList<PolicyResult>> HandleAsync(ListPoliciesQuery query, CancellationToken ct)
    {
        var all = await _policies.ListAsync(ct);
        return all.Select(PolicyResult.From).ToList();
    }
}'''
CS["appdi"] = r'''using Insurance.Application.Policies;
using Insurance.Domain;
using Microsoft.Extensions.DependencyInjection;

namespace Insurance.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IPremiumCalculator, DiscountedPremium>();
        services.AddScoped<CreatePolicyHandler>();
        services.AddScoped<CancelPolicyHandler>();
        services.AddScoped<GetPolicyHandler>();
        services.AddScoped<ListPoliciesHandler>();
        return services;
    }
}'''
CS["ctx"] = r'''using Insurance.Domain;
using Microsoft.EntityFrameworkCore;

namespace Insurance.Infrastructure;

public class InsuranceContext : DbContext
{
    public InsuranceContext(DbContextOptions<InsuranceContext> options) : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Policy> Policies => Set<Policy>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Customer>(e =>
        {
            e.Property(c => c.Name).HasMaxLength(100).IsRequired();
            e.Property(c => c.TaxId).HasMaxLength(9).IsRequired();
            e.HasIndex(c => c.TaxId).IsUnique();
        });

        modelBuilder.Entity<Policy>(e =>
        {
            e.Property(p => p.Number).HasMaxLength(20).IsRequired();
            e.HasIndex(p => p.Number).IsUnique();
            e.Property(p => p.Premium).HasPrecision(18, 2);
            e.Property(p => p.Status).HasConversion<string>().HasMaxLength(20);
            e.HasOne(p => p.Customer)
             .WithMany(c => c.Policies)
             .HasForeignKey(p => p.CustomerId);
        });
    }
}'''
CS["repo"] = r'''using Insurance.Application.Abstractions;
using Insurance.Domain;
using Microsoft.EntityFrameworkCore;

namespace Insurance.Infrastructure;

public class PolicyRepository : IPolicyRepository
{
    private readonly InsuranceContext _db;

    public PolicyRepository(InsuranceContext db) => _db = db;

    public Task<Policy?> GetByNumberAsync(string number, CancellationToken ct)
        => _db.Policies.Include(p => p.Customer)
                       .FirstOrDefaultAsync(p => p.Number == number, ct);

    public Task<bool> ExistsAsync(string number, CancellationToken ct)
        => _db.Policies.AnyAsync(p => p.Number == number, ct);

    public async Task<IReadOnlyList<Policy>> ListAsync(CancellationToken ct)
        => await _db.Policies.Include(p => p.Customer)
                             .AsNoTracking()
                             .OrderBy(p => p.Number)
                             .ToListAsync(ct);

    public async Task AddAsync(Policy policy, CancellationToken ct)
        => await _db.Policies.AddAsync(policy, ct);

    public Task SaveChangesAsync(CancellationToken ct)
        => _db.SaveChangesAsync(ct);
}

public class CustomerRepository : ICustomerRepository
{
    private readonly InsuranceContext _db;

    public CustomerRepository(InsuranceContext db) => _db = db;

    public Task<Customer?> GetByTaxIdAsync(string taxId, CancellationToken ct)
        => _db.Customers.Include(c => c.Policies)
                        .FirstOrDefaultAsync(c => c.TaxId == taxId, ct);
}'''
CS["infradi"] = r'''using Insurance.Application.Abstractions;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace Insurance.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<InsuranceContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("Insurance")));

        services.AddScoped<IPolicyRepository, PolicyRepository>();
        services.AddScoped<ICustomerRepository, CustomerRepository>();
        return services;
    }
}'''
CS["dto"] = r'''using System.ComponentModel.DataAnnotations;
using Insurance.Application.Policies;

namespace Insurance.Api.Policies;

public record NewPolicy(
    [property: Required, StringLength(20)] string Number,
    [property: Required, StringLength(100)] string CustomerName,
    [property: Required, RegularExpression(@"^\d{9}$")] string TaxId,
    [property: Range(0.01, 1_000_000)] decimal BasePremium);

public record PolicyResponse(string Number, string CustomerName, decimal Premium, DateOnly Start, string Status)
{
    public static PolicyResponse From(PolicyResult r)
        => new(r.Number, r.CustomerName, r.Premium, r.Start, r.Status);
}'''
CS["controller"] = r'''using Insurance.Application.Policies;
using Microsoft.AspNetCore.Mvc;

namespace Insurance.Api.Policies;

[ApiController]
[Route("api/[controller]")]
public class PoliciesController : ControllerBase
{
    private readonly CreatePolicyHandler _create;
    private readonly CancelPolicyHandler _cancel;
    private readonly GetPolicyHandler _get;
    private readonly ListPoliciesHandler _list;

    public PoliciesController(
        CreatePolicyHandler create, CancelPolicyHandler cancel,
        GetPolicyHandler get, ListPoliciesHandler list)
    {
        _create = create; _cancel = cancel; _get = get; _list = list;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<PolicyResponse>>> List(CancellationToken ct)
    {
        var result = await _list.HandleAsync(new ListPoliciesQuery(), ct);
        return Ok(result.Select(PolicyResponse.From));
    }

    [HttpGet("{number}")]
    public async Task<ActionResult<PolicyResponse>> Get(string number, CancellationToken ct)
    {
        var result = await _get.HandleAsync(new GetPolicyQuery(number), ct);
        return Ok(PolicyResponse.From(result));
    }

    [HttpPost]
    public async Task<ActionResult<PolicyResponse>> Create(NewPolicy body, CancellationToken ct)
    {
        var command = new CreatePolicyCommand(body.Number, body.CustomerName, body.TaxId, body.BasePremium);
        var result = await _create.HandleAsync(command, ct);

        return CreatedAtAction(nameof(Get), new { number = result.Number }, PolicyResponse.From(result));
    }

    [HttpDelete("{number}")]
    public async Task<IActionResult> Cancel(string number, CancellationToken ct)
    {
        await _cancel.HandleAsync(new CancelPolicyCommand(number), ct);
        return NoContent();
    }
}'''
CS["mw"] = r'''using Insurance.Application.Policies;
using Insurance.Domain;
using Microsoft.AspNetCore.Mvc;

namespace Insurance.Api;

public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionMiddleware> _logger;

    public ExceptionMiddleware(RequestDelegate next, ILogger<ExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            var status = ex switch
            {
                InvalidPolicyException => StatusCodes.Status400BadRequest,
                PolicyNotFoundException => StatusCodes.Status404NotFound,
                PolicyAlreadyExistsException => StatusCodes.Status409Conflict,
                _ => StatusCodes.Status500InternalServerError
            };

            if (status == StatusCodes.Status500InternalServerError)
                _logger.LogError(ex, "Unhandled error on {Path}", context.Request.Path);

            context.Response.StatusCode = status;
            await context.Response.WriteAsJsonAsync(new ProblemDetails
            {
                Status = status,
                Title = status == 500 ? "Unexpected error" : ex.Message
            });
        }
    }
}'''
CS["program"] = r'''using Insurance.Api;
using Insurance.Application;
using Insurance.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddOpenApi();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();   // first: catches everything below
if (app.Environment.IsDevelopment())
    app.MapOpenApi();
app.UseHttpsRedirection();
app.MapControllers();

app.Run();'''
CS["settings"] = r'''{
  "ConnectionStrings": {
    "Insurance": "Server=(localdb)\\MSSQLLocalDB;Database=Insurance;Trusted_Connection=True;TrustServerCertificate=True"
  },
  "Logging": {
    "LogLevel": { "Default": "Information", "Microsoft.AspNetCore": "Warning" }
  }
}'''
CS["tests"] = r'''using Insurance.Application.Abstractions;
using Insurance.Application.Policies;
using Insurance.Domain;
using NSubstitute;

namespace Insurance.Tests;

public class CreatePolicyHandlerTests
{
    private readonly IPolicyRepository _policies = Substitute.For<IPolicyRepository>();
    private readonly ICustomerRepository _customers = Substitute.For<ICustomerRepository>();
    private readonly CreatePolicyHandler _handler;

    public CreatePolicyHandlerTests()
        => _handler = new CreatePolicyHandler(_policies, _customers, new DiscountedPremium());

    private static CreatePolicyCommand NewCommand()
        => new("AP-001", "Ana Pereira", "123456789", 320.50m);

    [Fact]
    public async Task HandleAsync_NewPolicy_SavesAndReturnsResult()
    {
        _policies.ExistsAsync("AP-001", Arg.Any<CancellationToken>()).Returns(false);

        var result = await _handler.HandleAsync(NewCommand(), CancellationToken.None);

        Assert.Equal("AP-001", result.Number);
        Assert.Equal(320.50m, result.Premium);
        await _policies.Received(1).SaveChangesAsync(Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task HandleAsync_DuplicateNumber_ThrowsAndDoesNotSave()
    {
        _policies.ExistsAsync("AP-001", Arg.Any<CancellationToken>()).Returns(true);

        await Assert.ThrowsAsync<PolicyAlreadyExistsException>(
            () => _handler.HandleAsync(NewCommand(), CancellationToken.None));

        await _policies.DidNotReceive().SaveChangesAsync(Arg.Any<CancellationToken>());
    }
}

public class DiscountedPremiumTests
{
    [Theory]
    [InlineData(100, 0, 100)]
    [InlineData(100, 1, 90)]
    [InlineData(250, 3, 225)]
    public void Calculate_ReturnsExpectedPremium(int basePremium, int existing, int expected)
    {
        var calculator = new DiscountedPremium();

        Assert.Equal((decimal)expected, calculator.Calculate(basePremium, existing));
    }
}'''
CS["http"] = r'''POST https://localhost:5001/api/policies
Content-Type: application/json

{ "number": "AP-001", "customerName": "Ana Pereira", "taxId": "123456789", "basePremium": 320.50 }

# 201 Created
# Location: https://localhost:5001/api/policies/AP-001
# { "number": "AP-001", "customerName": "Ana Pereira", "premium": 320.50, "start": "2026-11-02", "status": "Active" }'''

MOD4 = dict(
 id="projeto", num=4, kind="project", title="Projeto final: API de apólices", short="Projeto final",
 tagline="Uma Web API construída de raiz com Clean Architecture, onde usas tudo o que aprendeste nos módulos anteriores.",
 brief=dict(
  context="Uma seguradora precisa de uma API para registar e consultar apólices. Constróis a solução de raiz, sem projeto de partida, com Domain, Application, Infrastructure, Api e Tests.",
  cards=[
   dict(t="O que constróis", d="Uma API com quatro endpoints sobre apólices, guardadas em SQL Server.",
        more=dict(more="Cada apólice pertence a um cliente identificado pelo NIF. Ao criar uma apólice para um cliente que já existe, ele é reutilizado e recebe 10% de desconto no prémio. Cancelar uma apólice não a apaga: muda o estado para Cancelled.")),
   dict(t="O que usas", d="C#, ASP.NET Core, Dependency Injection, EF Core, xUnit e Clean Architecture.",
        more=dict(more="Cada fase do projeto indica os capítulos que usa. Se te esqueceste de alguma coisa, o botão leva-te diretamente ao tema.")),
   dict(t="Como sabes que acabaste", d="Os endpoints respondem como descrito, os testes passam e explicas o percurso de um pedido.",
        more=dict(more="No fim da página tens a lista de critérios de aceitação. Marca cada um quando o conseguires demonstrar."))
  ]),
 layers=[
  dict(id="domain", name="Insurance.Domain", role="Regras do negócio", color="domain",
       has=["Customer, Policy, PolicyStatus", "IPremiumCalculator e DiscountedPremium", "InvalidPolicyException"],
       refs=[], never="EF Core, ASP.NET Core, ou qualquer outro projeto.",
       why="É o centro. Se uma regra do negócio muda (por exemplo, o desconto), só mexes aqui. Como não referencia nada, é rápido de testar e impossível de contaminar com detalhes técnicos."),
  dict(id="application", name="Insurance.Application", role="Casos de uso", color="application",
       has=["Commands, queries e handlers", "IPolicyRepository, ICustomerRepository", "PolicyResult e exceções de aplicação", "AddApplication()"],
       refs=["Insurance.Domain"], never="EF Core e ASP.NET Core.",
       why="Orquestra o Domain: valida se o número já existe, escolhe o cliente, calcula o prémio e manda guardar. As interfaces dos repositórios vivem aqui porque quem as usa é que define o contrato."),
  dict(id="infrastructure", name="Insurance.Infrastructure", role="Base de dados", color="infra",
       has=["InsuranceContext e migrations", "PolicyRepository, CustomerRepository", "AddInfrastructure()"],
       refs=["Insurance.Application"], never="A camada Api.",
       why="Implementa os contratos da Application com o EF Core. Trocar de base de dados é escrever outra implementação aqui, sem tocar nos handlers."),
  dict(id="api", name="Insurance.Api", role="HTTP", color="api",
       has=["PoliciesController e DTOs", "ExceptionMiddleware", "Program.cs e appsettings.json"],
       refs=["Insurance.Application", "Insurance.Infrastructure"], never="Lógica de negócio.",
       why="Traduz HTTP em comandos e consultas e devolve o código de estado certo. Referencia a Infrastructure só para a registar no container."),
  dict(id="tests", name="Insurance.Tests", role="Verificação", color="tests",
       has=["Testes dos handlers com mocks", "Testes do cálculo do prémio"],
       refs=["Insurance.Domain", "Insurance.Application"], never="Base de dados real.",
       why="Testa os handlers sem base de dados nem HTTP, porque dependem de interfaces. Corre em segundos."),
 ],
 flow=[
  dict(layer="api", t="Pedido chega", d="POST /api/policies com o JSON. O ASP.NET Core converte-o em NewPolicy e valida os atributos; se estiver inválido, responde 400 sem chegar ao controller."),
  dict(layer="api", t="Controller", d="Cria o CreatePolicyCommand e chama o CreatePolicyHandler. É tudo o que o controller faz."),
  dict(layer="application", t="Handler", d="Verifica se o número já existe (senão, lança PolicyAlreadyExistsException), vai buscar ou cria o cliente e calcula o prémio."),
  dict(layer="domain", t="Domain", d="Policy.Create valida as regras: número preenchido e prémio positivo. Uma violação lança InvalidPolicyException."),
  dict(layer="infrastructure", t="Repositório", d="AddAsync marca a apólice para inserir e SaveChangesAsync gera o INSERT numa transação."),
  dict(layer="api", t="Resposta", d="CreatedAtAction devolve 201 com o cabeçalho Location. Se alguma exceção subiu, o ExceptionMiddleware converte-a em 400, 404, 409 ou 500."),
 ],
 phases=[
  dict(id="p1", title="Montar a solução", goal="Criar a estrutura de pastas, os cinco projetos e as referências, pela ordem certa.",
       uses=["dotnet-1"],
       steps=["Criar a pasta Insurance e a solução", "Criar os projetos: Domain, Application, Infrastructure, Api (controllers) e Tests", "Adicionar todos à solução", "Referenciar os projetos pela regra das dependências", "Instalar os pacotes e a ferramenta dotnet-ef", "Compilar"],
       files=[dict(name="Terminal", lang="sh", code=r'''mkdir Insurance && cd Insurance
dotnet new sln -n Insurance

dotnet new classlib -n Insurance.Domain         -o src/Insurance.Domain
dotnet new classlib -n Insurance.Application    -o src/Insurance.Application
dotnet new classlib -n Insurance.Infrastructure -o src/Insurance.Infrastructure
dotnet new webapi --use-controllers -n Insurance.Api -o src/Insurance.Api
dotnet new xunit    -n Insurance.Tests          -o tests/Insurance.Tests

dotnet sln add src/Insurance.Domain src/Insurance.Application src/Insurance.Infrastructure src/Insurance.Api tests/Insurance.Tests

dotnet add src/Insurance.Application    reference src/Insurance.Domain
dotnet add src/Insurance.Infrastructure reference src/Insurance.Application
dotnet add src/Insurance.Api            reference src/Insurance.Application src/Insurance.Infrastructure
dotnet add tests/Insurance.Tests        reference src/Insurance.Domain src/Insurance.Application

dotnet add src/Insurance.Application    package Microsoft.Extensions.DependencyInjection.Abstractions
dotnet add src/Insurance.Infrastructure package Microsoft.EntityFrameworkCore.SqlServer
dotnet add src/Insurance.Api            package Microsoft.EntityFrameworkCore.Design
dotnet add tests/Insurance.Tests        package NSubstitute
dotnet tool install --global dotnet-ef   # only if you did not install it already

dotnet build''')],
       check="Build succeeded.\n    0 Warning(s)\n    0 Error(s)",
       more=dict(more="As referências são a arquitetura. Repara que o Domain não tem nenhuma, a Application só referencia o Domain e a Infrastructure só referencia a Application. A Api referencia a Infrastructure apenas para a registar no Program.cs.\n\nApaga os ficheiros de exemplo que os templates geram (Class1.cs, WeatherForecast.cs, WeatherForecastController.cs, UnitTest1.cs).", pit="Se o dotnet sln add não aceitar pastas na tua versão, indica o caminho completo de cada .csproj.", tryit="Corre tree -I 'bin|obj' (ou tree /f no Windows) e compara com a estrutura da Clean Architecture."),
       ),
  dict(id="p2", title="Domain", goal="Escrever as entidades e as regras de negócio, sem depender de nada.",
       uses=["csharp-2", "csharp-3"],
       steps=["Criar Customer, Policy e PolicyStatus com setters privados", "Validar as regras na criação (número, prémio, NIF)", "Criar InvalidPolicyException", "Criar IPremiumCalculator e DiscountedPremium"],
       files=[dict(name="Insurance.Domain/Policies.cs", lang="cs", code=CS["domain"]), dict(name="Insurance.Domain/PremiumCalculator.cs", lang="cs", code=CS["calc"])],
       check="dotnet build src/Insurance.Domain\nBuild succeeded.",
       more=dict(more="As entidades têm construtor privado sem parâmetros porque o EF Core precisa dele para criar objetos ao ler da base de dados. Quem cria uma Policy usa Policy.Create, que garante as regras: é impossível criar uma apólice com prémio negativo.\n\nOs setters privados fazem com que o estado só mude através dos métodos da própria classe (como Cancel).", pit="Pôr atributos do EF Core (como [Key]) nas entidades. O Domain não deve conhecer o EF Core; a configuração fica na Infrastructure.", tryit="Escreve já um teste para Policy.Create com prémio 0. Deve lançar InvalidPolicyException."),
       ),
  dict(id="p3", title="Application", goal="Escrever os casos de uso como comandos, consultas e handlers, dependendo só de interfaces.",
       uses=["dotnet-3", "dotnet-6", "csharp-3"],
       steps=["Declarar IPolicyRepository e ICustomerRepository", "Criar CreatePolicyCommand, o resultado e CreatePolicyHandler", "Criar GetPolicy, ListPolicies e CancelPolicy", "Registar tudo em AddApplication()"],
       files=[dict(name="Insurance.Application/Abstractions.cs", lang="cs", code=CS["abstr"]), dict(name="Insurance.Application/Policies/CreatePolicy.cs", lang="cs", code=CS["create"]), dict(name="Insurance.Application/Policies/Queries.cs", lang="cs", code=CS["queries"]), dict(name="Insurance.Application/DependencyInjection.cs", lang="cs", code=CS["appdi"])],
       check="dotnet build src/Insurance.Application\nBuild succeeded.",
       more=dict(more="O comando é só dados; o handler tem a lógica do caso de uso e depende de interfaces, por isso não sabe nada de EF Core. Repara na separação: o handler decide (já existe? desconto?) e o Domain valida (prémio positivo?).\n\nCancelPolicy é um comando que não devolve dados; GetPolicy e ListPolicies são consultas que só leem. É a regra do CQRS.", pit="Esquecer de registar um handler em AddApplication(). O erro só aparece no primeiro pedido, quando o container não consegue criar o controller.", tryit="Acrescenta a consulta ListCustomerPolicies, com o seu handler (é o extra do capítulo de Organização do código)."),
       ),
  dict(id="p4", title="Infrastructure", goal="Implementar os repositórios com o EF Core, configurar o modelo e criar a base de dados.",
       uses=["dotnet-4", "csharp-3"],
       steps=["Criar o InsuranceContext e configurar o modelo com a Fluent API", "Implementar PolicyRepository e CustomerRepository", "Criar AddInfrastructure()", "Pôr a connection string no appsettings.json da Api", "Criar a primeira migration e aplicá-la"],
       files=[dict(name="Insurance.Infrastructure/InsuranceContext.cs", lang="cs", code=CS["ctx"]), dict(name="Insurance.Infrastructure/Repositories.cs", lang="cs", code=CS["repo"]), dict(name="Insurance.Infrastructure/DependencyInjection.cs", lang="cs", code=CS["infradi"]), dict(name="Insurance.Api/appsettings.json", lang="json", code=CS["settings"]), dict(name="Terminal", lang="sh", code=r'''dotnet ef migrations add InitialCreate -p src/Insurance.Infrastructure -s src/Insurance.Api
dotnet ef database update            -p src/Insurance.Infrastructure -s src/Insurance.Api''')],
       check="Applying migration '20261102120000_InitialCreate'.\nDone.",
       more=dict(more="Os dois parâmetros dos comandos dotnet ef têm papéis diferentes: -p é o projeto onde está o DbContext e onde ficam as migrations (Infrastructure); -s é o projeto de arranque, de onde se lê a configuração (Api). Por isso o pacote Design foi instalado na Api.\n\nDepois de aplicar, abre o cliente SQL e confirma as tabelas Customers, Policies e __EFMigrationsHistory, com índices únicos em Policies.Number e Customers.TaxId.", pit="Correr dotnet ef a partir da pasta errada ou sem -s. A mensagem diz que não encontra o DbContext ou a connection string.", tryit="Abre o ficheiro da migration e identifica o que o Up cria. Depois confirma o tipo da coluna Premium (decimal(18,2))."),
       ),
  dict(id="p5", title="Api", goal="Expor os casos de uso por HTTP, com DTOs, validação, tratamento de erros e documentação.",
       uses=["dotnet-2", "dotnet-3", "csharp-3"],
       steps=["Criar os DTOs NewPolicy e PolicyResponse com validação", "Criar o PoliciesController com os quatro endpoints", "Criar o ExceptionMiddleware que traduz exceções em códigos HTTP", "Montar o Program.cs", "Correr a API e abrir o documento OpenAPI"],
       files=[dict(name="Insurance.Api/Policies/Dtos.cs", lang="cs", code=CS["dto"]), dict(name="Insurance.Api/Policies/PoliciesController.cs", lang="cs", code=CS["controller"]), dict(name="Insurance.Api/ExceptionMiddleware.cs", lang="cs", code=CS["mw"]), dict(name="Insurance.Api/Program.cs", lang="cs", code=CS["program"]), dict(name="Terminal", lang="sh", code="dotnet run --project src/Insurance.Api")],
       check="Now listening on: https://localhost:5xxx\nGET /openapi/v1.json -> 200",
       more=dict(more="O controller não tem if nem try/catch. Quando uma regra falha, o handler ou o Domain lança uma exceção e o middleware converte-a no código HTTP certo, com um ProblemDetails. O Program.cs regista o middleware primeiro para apanhar tudo o que vem a seguir.\n\nOs dois métodos de registo (AddApplication e AddInfrastructure) são o único sítio onde a Api conhece as implementações concretas.", pit="Registar o ExceptionMiddleware depois do MapControllers. Os erros deixam de ser apanhados.", tryit="Faz um POST com taxId \"123\". Que código recebes: o 400 do atributo de validação ou o do Domain? Porquê?"),
       ),
  dict(id="p6", title="Testes", goal="Provar os handlers e as regras sem base de dados nem HTTP.",
       uses=["dotnet-5"],
       steps=["Testar CreatePolicyHandler com mocks dos repositórios", "Testar o caso do número duplicado", "Testar DiscountedPremium com um Theory", "Correr todos os testes"],
       files=[dict(name="Insurance.Tests/CreatePolicyHandlerTests.cs", lang="cs", code=CS["tests"]), dict(name="Terminal", lang="sh", code="dotnet test")],
       check="Passed!  - Failed:     0,\n           Passed:     4,\n           Skipped:    0,\n           Total:      4",
       more=dict(more="Os testes dos handlers são rápidos porque os repositórios são falsos. O de duplicado confirma duas coisas: a exceção certa e que SaveChangesAsync não foi chamado (DidNotReceive).\n\nO Theory cobre o desconto com e sem clientes anteriores. Os valores são int porque os atributos não aceitam decimal; converte-se para decimal dentro do teste.", tryit="Escreve um teste a CancelPolicyHandler que verifica a PolicyNotFoundException quando o número não existe."),
       ),
  dict(id="p7", title="Verificar", goal="Experimentar a API como um cliente e confirmar todos os casos.",
       uses=["dotnet-2"],
       steps=["Criar uma coleção no Bruno ou no Postman (ou importar o documento OpenAPI)", "POST de uma apólice válida: espera 201", "Repetir o mesmo POST: espera 409", "GET de um número inexistente: espera 404", "POST com NIF inválido: espera 400", "DELETE de uma apólice: espera 204 e estado Cancelled no GET seguinte"],
       files=[dict(name="Pedido de exemplo", lang="http", code=CS["http"])],
       check="POST   -> 201   repetido -> 409\nGET    -> 200   inexistente -> 404\nDELETE -> 204   NIF inválido -> 400",
       more=dict(more="Este é o teste que o utilizador final faria. Guarda os pedidos na coleção: ficam como documentação viva da API e podes voltar a corrê-los depois de qualquer alteração.", tryit="Cria duas apólices para o mesmo NIF e confirma que a segunda tem 10% de desconto."),
       ),
 ],
 endpoints=[["Pedido", "Sucesso", "Erros"],
            ["GET /api/policies", "200 com a lista", "—"],
            ["GET /api/policies/{number}", "200 com a apólice", "404 se não existir"],
            ["POST /api/policies", "201 com Location", "400 se inválido; 409 se repetida"],
            ["DELETE /api/policies/{number}", "204 sem corpo", "404 se não existir; 400 se já cancelada"]],
 accept=[
  "A solução compila sem avisos",
  "O Domain não referencia nenhum projeto nem pacote do EF Core",
  "As migrations criam as tabelas e os índices únicos",
  "Os quatro endpoints respondem como na tabela de endpoints",
  "Os erros chegam em ProblemDetails e nunca como exceção sem tratamento",
  "Os testes dos handlers e do cálculo passam",
  "Consigo explicar o percurso de um POST, do pedido à base de dados",
  "Consigo explicar porque a interface do repositório fica na Application"],
 extras=[
  "Acrescentar ListCustomerPolicies: todas as apólices de um NIF",
  "Registar com ILogger uma mensagem com {Number} quando uma apólice é criada",
  "Aceitar um filtro opcional ?status=Active no GET /api/policies",
 ])
