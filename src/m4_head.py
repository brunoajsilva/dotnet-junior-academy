# -*- coding: utf-8 -*-
# Module 4: BankingApp final project (6 days). Code is C# 14 / .NET 10, identifiers in English.
F = {}   # code files

# ============================================================ STEP 1
F["s1_sh"] = r'''# NuGet packages (or use the NuGet window of the IDE)
dotnet add src/BankingApp.Application    package Microsoft.Extensions.DependencyInjection.Abstractions
dotnet add src/BankingApp.Infrastructure package Microsoft.EntityFrameworkCore.SqlServer
dotnet add src/BankingApp.Api            package Microsoft.EntityFrameworkCore.Design
dotnet add src/BankingApp.Api            package Swashbuckle.AspNetCore.SwaggerUI
dotnet add tests/BankingApp.Tests        package NSubstitute

# the EF Core command-line tool, once per machine
dotnet tool install --global dotnet-ef'''

F["s1_mkdir"] = r'''BankingApp.Domain          (sem referências)
BankingApp.Application     -> BankingApp.Domain
BankingApp.Infrastructure  -> BankingApp.Application
BankingApp.Api             -> BankingApp.Application, BankingApp.Infrastructure
BankingApp.Tests           -> BankingApp.Domain, BankingApp.Application'''

F["domain_exc"] = r'''namespace BankingApp.Domain.Common;

public class DomainException : Exception
{
    public DomainException(string message) : base(message) { }
}'''

F["resp_empty"] = r'''namespace BankingApp.Application.Common;

// the data of a use case that returns nothing: Response<Empty>
public sealed class Empty
{
}'''

F["cust_command"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

// command: only data
public class CreateCustomerCommand : Request
{
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";
}'''

F["cust_result"] = r'''using BankingApp.Domain.Customers;

namespace BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

public class CustomerResult
{
    public int Id { get; init; }
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";

    public static CustomerResult From(Customer customer) => new()
    {
        Id = customer.Id,
        Name = customer.Name,
        TaxId = customer.TaxId
    };
}'''

F["list_query"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.QueryHandlers.ListCustomers;

public class ListCustomersQuery : Request
{
}'''

F["contracts1b"] = r'''using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;


namespace BankingApp.Api.Contracts.Customers;

public class CustomerResponse
{
    public int Id { get; init; }
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";

    public static CustomerResponse From(CustomerResult result) => new()
    {
        Id = result.Id,
        Name = result.Name,
        TaxId = result.TaxId
    };
}'''

F["account_status"] = r'''namespace BankingApp.Domain.Accounts;

public enum AccountStatus
{
    Active,
    Closed
}'''

F["hasher_if"] = r'''namespace BankingApp.Application.Abstractions;

public interface IPasswordHasher
{
    string Hash(string password);
    bool Verify(string hash, string password);
}'''

F["token_result"] = r'''namespace BankingApp.Application.Abstractions;

public class TokenResult
{
    public string AccessToken { get; init; } = "";
    public DateTime ExpiresAtUtc { get; init; }
}'''

F["token_if"] = r'''using BankingApp.Domain.Customers;

namespace BankingApp.Application.Abstractions;

public interface ITokenService
{
    TokenResult Create(Customer customer);
}'''

F["reg_command"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.Register;

public class RegisterCommand : Request
{
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";
    public string Email { get; init; } = "";
    public string Password { get; init; } = "";
}'''

F["reg_result"] = r'''
namespace BankingApp.Application.Handlers.CommandHandlers.Register;

public class RegisterResult
{
    public int CustomerId { get; init; }
    public string AccountNumber { get; init; } = "";
}'''

F["login_command"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.Login;

public class LoginCommand : Request
{
    public string Email { get; init; } = "";
    public string Password { get; init; } = "";
}'''

F["login_result"] = r'''
namespace BankingApp.Application.Handlers.CommandHandlers.Login;

public class LoginResult
{
    public string AccessToken { get; init; } = "";
    public DateTime ExpiresAtUtc { get; init; }
}'''

F["dash_query"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class RetrieveDashboardQuery : Request
{
    public int CustomerId { get; init; }
}'''

F["dash_account"] = r'''
namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class DashboardAccount
{
    public string Number { get; init; } = "";
    public decimal Balance { get; init; }
    public string Status { get; init; } = "";
    public DateOnly Opened { get; init; }
}'''

F["dash_result"] = r'''
namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class DashboardResult
{
    public string CustomerName { get; init; } = "";
    public string Email { get; init; } = "";
    public decimal TotalBalance { get; init; }
    public IReadOnlyList<DashboardAccount> Accounts { get; init; } = [];
}'''

F["reg_resp"] = r'''using BankingApp.Application.Handlers.CommandHandlers.Register;


namespace BankingApp.Api.Contracts.Auth;

public class RegisterResponse
{
    public int CustomerId { get; init; }
    public string AccountNumber { get; init; } = "";

    public static RegisterResponse From(RegisterResult result) => new()
    {
        CustomerId = result.CustomerId,
        AccountNumber = result.AccountNumber
    };
}'''

F["login_req"] = r'''using System.ComponentModel.DataAnnotations;

namespace BankingApp.Api.Contracts.Auth;

public class LoginRequest
{
    [Required, EmailAddress]
    public string Email { get; set; } = "";

    [Required]
    public string Password { get; set; } = "";
}'''

F["login_resp"] = r'''using BankingApp.Application.Handlers.CommandHandlers.Login;


namespace BankingApp.Api.Contracts.Auth;

public class LoginResponse
{
    public string AccessToken { get; init; } = "";
    public DateTime ExpiresAtUtc { get; init; }

    public static LoginResponse From(LoginResult result) => new()
    {
        AccessToken = result.AccessToken,
        ExpiresAtUtc = result.ExpiresAtUtc
    };
}'''

F["dash_acc_resp"] = r'''using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;


namespace BankingApp.Api.Contracts.Dashboard;

public class DashboardAccountResponse
{
    public string Number { get; init; } = "";
    public decimal Balance { get; init; }
    public string Status { get; init; } = "";
    public DateOnly Opened { get; init; }

    public static DashboardAccountResponse From(DashboardAccount account) => new()
    {
        Number = account.Number,
        Balance = account.Balance,
        Status = account.Status,
        Opened = account.Opened
    };
}'''

F["dash_resp"] = r'''using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;


namespace BankingApp.Api.Contracts.Dashboard;

public class DashboardResponse
{
    public string CustomerName { get; init; } = "";
    public string Email { get; init; } = "";
    public decimal TotalBalance { get; init; }
    public IReadOnlyList<DashboardAccountResponse> Accounts { get; init; } = [];

    public static DashboardResponse From(DashboardResult result) => new()
    {
        CustomerName = result.CustomerName,
        Email = result.Email,
        TotalBalance = result.TotalBalance,
        Accounts = result.Accounts.Select(DashboardAccountResponse.From).ToList()
    };
}'''

F["customer1"] = r'''using BankingApp.Domain.Common;

namespace BankingApp.Domain.Customers;

public class Customer
{
    private Customer() { }   // required by EF Core

    public Customer(string name, string taxId)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Name is required.");
        if (taxId.Length != 9 || !taxId.All(char.IsDigit))
            throw new DomainException($"Invalid tax id: {taxId}");

        Name = name.Trim();
        TaxId = taxId;
    }

    public int Id { get; private set; }
    public string Name { get; private set; } = "";
    public string TaxId { get; private set; } = "";
}'''

F["app_exc"] = r'''namespace BankingApp.Application.Common;

// RPC: errors are data. Every use case answers with a list of Error, never with an HTTP code.
public class Error
{
    public Error(string code, string message)
    {
        Code = code;
        Message = message;
    }

    public string Code { get; }
    public string Message { get; }

    public static Error Validation(string message)   => new("validation", message);
    public static Error NotFound(string message)     => new("not_found", message);
    public static Error Conflict(string message)     => new("conflict", message);
    public static Error Unauthorized(string message) => new("unauthorized", message);
    public static Error Forbidden(string message)    => new("forbidden", message);
    public static Error Unexpected()                 => new("unexpected", "Unexpected error.");
}'''

F["resp_request"] = r'''namespace BankingApp.Application.Common;

// every input of a use case (command or query) derives from Request
public abstract class Request
{
}'''

F["resp_response"] = r'''namespace BankingApp.Application.Common;

// the output of EVERY use case: success is just "no errors"
public class Response<T>
{
    public bool Success => Errors.Count == 0;
    public T? Data { get; init; }
    public IReadOnlyList<Error> Errors { get; init; } = [];

    public static Response<T> Ok(T data) => new() { Data = data };

    public static Response<T> Fail(params IEnumerable<Error> errors)
        => new() { Errors = errors.ToList() };

    // convert the data (for example, a result into a DTO) and keep the errors
    public Response<TOut> Map<TOut>(Func<T, TOut> map)
        => Success ? Response<TOut>.Ok(map(Data!)) : Response<TOut>.Fail(Errors);
}'''

F["resp_handler"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Application.Abstractions;

// one handler per use case: a Request goes in, a Response comes out
public interface IHandler<in TRequest, TData> where TRequest : Request
{
    Task<Response<TData>> HandleAsync(TRequest request, CancellationToken ct);
}'''

F["repo_if1"] = r'''using BankingApp.Domain.Customers;

namespace BankingApp.Application.Abstractions;

public interface ICustomerRepository
{
    Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct);
    Task<IReadOnlyList<Customer>> ListAsync(CancellationToken ct);
    Task AddAsync(Customer customer, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}'''

F["create_customer"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Domain.Customers;

namespace BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

// handler: the use case. Business errors come back in the Response, they are not thrown
public class CreateCustomerHandler : IHandler<CreateCustomerCommand, CustomerResult>
{
    private readonly ICustomerRepository _customers;

    public CreateCustomerHandler(ICustomerRepository customers) => _customers = customers;

    public async Task<Response<CustomerResult>> HandleAsync(CreateCustomerCommand request, CancellationToken ct)
    {
        if (await _customers.ExistsByTaxIdAsync(request.TaxId, ct))
            return Response<CustomerResult>.Fail(
                Error.Conflict($"A customer with tax id {request.TaxId} already exists."));

        var customer = new Customer(request.Name, request.TaxId);

        await _customers.AddAsync(customer, ct);
        await _customers.SaveChangesAsync(ct);

        return Response<CustomerResult>.Ok(CustomerResult.From(customer));
    }
}'''

F["list_customers"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

namespace BankingApp.Application.Handlers.QueryHandlers.ListCustomers;

public class ListCustomersHandler : IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>>
{
    private readonly ICustomerRepository _customers;

    public ListCustomersHandler(ICustomerRepository customers) => _customers = customers;

    public async Task<Response<IReadOnlyList<CustomerResult>>> HandleAsync(ListCustomersQuery request, CancellationToken ct)
    {
        var all = await _customers.ListAsync(ct);
        return Response<IReadOnlyList<CustomerResult>>.Ok(all.Select(CustomerResult.From).ToList());
    }
}'''

F["app_di1"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;
using BankingApp.Application.Handlers.QueryHandlers.ListCustomers;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IHandler<CreateCustomerCommand, CustomerResult>, CreateCustomerHandler>();
        services.AddScoped<IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>>, ListCustomersHandler>();
        return services;
    }
}'''

F["ctx1"] = r'''using BankingApp.Domain.Customers;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Persistence;

public class BankingAppContext : DbContext
{
    public BankingAppContext(DbContextOptions<BankingAppContext> options) : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
        => modelBuilder.ApplyConfigurationsFromAssembly(typeof(BankingAppContext).Assembly);
}'''

F["cfg_customer1"] = r'''using BankingApp.Domain.Customers;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace BankingApp.Infrastructure.Persistence.Configurations;

public class CustomerConfiguration : IEntityTypeConfiguration<Customer>
{
    public void Configure(EntityTypeBuilder<Customer> builder)
    {
        builder.Property(c => c.Name).HasMaxLength(100).IsRequired();
        builder.Property(c => c.TaxId).HasMaxLength(9).IsRequired();
        builder.HasIndex(c => c.TaxId).IsUnique();
    }
}'''

F["repo1"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Domain.Customers;
using BankingApp.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Repositories;

public class CustomerRepository : ICustomerRepository
{
    private readonly BankingAppContext _db;

    public CustomerRepository(BankingAppContext db) => _db = db;

    public Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct)
        => _db.Customers.AnyAsync(c => c.TaxId == taxId, ct);

    public async Task<IReadOnlyList<Customer>> ListAsync(CancellationToken ct)
        => await _db.Customers.AsNoTracking().OrderBy(c => c.Name).ToListAsync(ct);

    public async Task AddAsync(Customer customer, CancellationToken ct)
        => await _db.Customers.AddAsync(customer, ct);

    public Task SaveChangesAsync(CancellationToken ct)
        => _db.SaveChangesAsync(ct);
}'''

F["infra_di1"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Infrastructure.Persistence;
using BankingApp.Infrastructure.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<BankingAppContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("BankingApp")));

        services.AddScoped<ICustomerRepository, CustomerRepository>();
        return services;
    }
}'''

F["mig1"] = r'''dotnet ef migrations add InitialCreate -p src/BankingApp.Infrastructure -s src/BankingApp.Api -o Persistence/Migrations
dotnet ef database update            -p src/BankingApp.Infrastructure -s src/BankingApp.Api'''

F["contracts1"] = r'''using System.ComponentModel.DataAnnotations;

namespace BankingApp.Api.Contracts.Customers;

public class NewCustomer
{
    [Required, StringLength(100)]
    public string Name { get; set; } = "";

    [Required, RegularExpression(@"^\d{9}$")]
    public string TaxId { get; set; } = "";
}'''

F["ctrl_customers"] = r'''using BankingApp.Api.Contracts.Customers;
using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;
using BankingApp.Application.Handlers.QueryHandlers.ListCustomers;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CustomersController : ControllerBase
{
    private readonly IHandler<CreateCustomerCommand, CustomerResult> _create;
    private readonly IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>> _list;

    public CustomersController(
        IHandler<CreateCustomerCommand, CustomerResult> create,
        IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>> list)
    {
        _create = create;
        _list = list;
    }

    // RPC: every operation is a POST to /api/<area>/<action>, and the answer is always 200 OK.
    // Read "success" and "errors" in the body.
    [HttpPost("list")]
    public async Task<Response<IEnumerable<CustomerResponse>>> List(CancellationToken ct)
    {
        var result = await _list.HandleAsync(new ListCustomersQuery(), ct);
        return result.Map(items => items.Select(CustomerResponse.From));
    }

    [HttpPost("create")]
    public async Task<Response<CustomerResponse>> Create(NewCustomer body, CancellationToken ct)
    {
        var result = await _create.HandleAsync(new CreateCustomerCommand { Name = body.Name, TaxId = body.TaxId }, ct);
        return result.Map(CustomerResponse.From);
    }
}'''

F["mw1"] = r'''using BankingApp.Application.Common;
using BankingApp.Domain.Common;

namespace BankingApp.Api.Middleware;

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
            Error error;

            if (ex is DomainException)
            {
                error = Error.Validation(ex.Message);   // a rule of the Domain refused the data
            }
            else
            {
                _logger.LogError(ex, "Unhandled error on {Path}", context.Request.Path);
                error = Error.Unexpected();              // never leak the details to the client
            }

            // RPC: the call reached the server, so the HTTP answer is always 200
            context.Response.StatusCode = StatusCodes.Status200OK;
            await context.Response.WriteAsJsonAsync(Response<object>.Fail(error));
        }
    }
}

// An exception is for the unexpected. Expected errors (not found, conflict)
// are returned by the handlers, as Response.Fail(...).'''

F["program1"] = r'''using BankingApp.Api.Middleware;
using BankingApp.Api.Responses;
using BankingApp.Application;
using BankingApp.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers()
    .ConfigureApiBehaviorOptions(o =>
        o.InvalidModelStateResponseFactory = ValidationResponse.Create);   // invalid DTO -> 200 + errors
builder.Services.AddOpenApi();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();   // first: catches everything below

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();                        // /openapi/v1.json
    app.UseSwaggerUI(o => o.SwaggerEndpoint("/openapi/v1.json", "v1"));   // /swagger
}

app.UseHttpsRedirection();
app.MapControllers();

app.Run();'''

F["settings1"] = r'''{
  "ConnectionStrings": {
    "BankingApp": "Server=(localdb)\\MSSQLLocalDB;Database=BankingApp;Trusted_Connection=True;TrustServerCertificate=True"
  },
  "Logging": {
    "LogLevel": { "Default": "Information", "Microsoft.AspNetCore": "Warning" }
  },
  "AllowedHosts": "*"
}'''

F["validation_resp"] = r'''using BankingApp.Application.Common;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Responses;

public static class ValidationResponse
{
    // [ApiController] would answer 400 + ProblemDetails when the DTO is invalid.
    // In an RPC API, we answer 200 and put every invalid field in the errors list.
    public static IActionResult Create(ActionContext context)
    {
        var errors = context.ModelState
            .Where(entry => entry.Value is { Errors.Count: > 0 })
            .SelectMany(entry => entry.Value!.Errors
                .Select(e => Error.Validation($"{entry.Key}: {e.ErrorMessage}")))
            .ToList();

        return new OkObjectResult(Response<object>.Fail(errors));
    }
}'''

F["launch"] = r'''"launchUrl": "swagger",'''

F["tests1"] = r'''using BankingApp.Domain.Common;
using BankingApp.Domain.Customers;

namespace BankingApp.Tests.Domain;

public class CustomerTests
{
    [Theory]
    [InlineData("123")]
    [InlineData("12345678a")]
    [InlineData("1234567890")]
    public void Constructor_InvalidTaxId_Throws(string taxId)
        => Assert.Throws<DomainException>(() => new Customer("Ana Pereira", taxId));

    [Fact]
    public void Constructor_ValidData_TrimsTheName()
    {
        var customer = new Customer("  Ana Pereira ", "123456789");

        Assert.Equal("Ana Pereira", customer.Name);
    }
}'''

F["tests_resp"] = r'''using BankingApp.Application.Common;

namespace BankingApp.Tests.Application;

public class ResponseTests
{
    [Fact]
    public void Ok_HasDataAndNoErrors()
    {
        var response = Response<int>.Ok(42);

        Assert.True(response.Success);
        Assert.Equal(42, response.Data);
        Assert.Empty(response.Errors);
    }

    [Fact]
    public void Fail_IsNotSuccessAndKeepsAllErrors()
    {
        var response = Response<int>.Fail(Error.Validation("a"), Error.Conflict("b"));

        Assert.False(response.Success);
        Assert.Equal(2, response.Errors.Count);
    }

    [Fact]
    public void Map_OnFailure_KeepsTheErrors()
    {
        var response = Response<int>.Fail(Error.NotFound("x")).Map(n => n.ToString());

        Assert.False(response.Success);
        Assert.Equal("not_found", response.Errors[0].Code);
    }
}'''

F["http1"] = r'''POST https://localhost:5001/api/customers/create
Content-Type: application/json

{ "name": "Ana Pereira", "taxId": "123456789" }

# 200 OK
# { "success": true, "errors": [], "data": { "id": 1, "name": "Ana Pereira", "taxId": "123456789" } }
#
# repeat the same request -> still 200 OK, but the body says it failed
# { "success": false,
#   "errors": [ { "code": "conflict", "message": "A customer with tax id 123456789 already exists." } ],
#   "data": null }'''

# ============================================================ STEP 2
F["s2_pk"] = r'''dotnet add src/BankingApp.Api            package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add src/BankingApp.Infrastructure package System.IdentityModel.Tokens.Jwt
dotnet add src/BankingApp.Infrastructure package Microsoft.Extensions.Identity.Core
dotnet add src/BankingApp.Infrastructure package Microsoft.Extensions.Options.ConfigurationExtensions'''

F["secrets2"] = r'''{
  "Jwt": {
    "Key": "replace-with-a-random-text-of-at-least-32-characters"
  }
}'''

F["settings2"] = r'''{
  "ConnectionStrings": {
    "BankingApp": "Server=(localdb)\\MSSQLLocalDB;Database=BankingApp;Trusted_Connection=True;TrustServerCertificate=True"
  },
  "Jwt": {
    "Issuer": "BankingApp",
    "Audience": "BankingApp.Clients",
    "Key": "replace-with-a-random-text-of-at-least-32-characters",
    "ExpiresMinutes": 60
  },
  "Logging": {
    "LogLevel": { "Default": "Information", "Microsoft.AspNetCore": "Warning" }
  },
  "AllowedHosts": "*"
}'''

F["customer2"] = r'''using BankingApp.Domain.Accounts;
using BankingApp.Domain.Common;

namespace BankingApp.Domain.Customers;

public class Customer
{
    private Customer() { }   // required by EF Core

    public Customer(string name, string taxId, string email, string passwordHash)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Name is required.");
        if (taxId.Length != 9 || !taxId.All(char.IsDigit))
            throw new DomainException($"Invalid tax id: {taxId}");
        if (!email.Contains('@'))
            throw new DomainException("Invalid email.");
        if (string.IsNullOrWhiteSpace(passwordHash))
            throw new DomainException("Password hash is required.");

        Name = name.Trim();
        TaxId = taxId;
        Email = email.Trim().ToLowerInvariant();
        PasswordHash = passwordHash;
    }

    public int Id { get; private set; }
    public string Name { get; private set; } = "";
    public string TaxId { get; private set; } = "";
    public string Email { get; private set; } = "";
    public string PasswordHash { get; private set; } = "";
    public List<Account> Accounts { get; private set; } = [];
}'''

F["account"] = r'''using BankingApp.Domain.Common;
using BankingApp.Domain.Customers;

namespace BankingApp.Domain.Accounts;

public class Account
{
    private Account() { }   // required by EF Core

    public static Account Open(string number, Customer customer, decimal initialDeposit, DateOnly opened)
    {
        if (string.IsNullOrWhiteSpace(number))
            throw new DomainException("Number is required.");
        if (initialDeposit < 0)
            throw new DomainException("Initial deposit cannot be negative.");

        return new Account
        {
            Number = number,
            Customer = customer,
            Balance = initialDeposit,
            Opened = opened,
            Status = AccountStatus.Active
        };
    }

    public int Id { get; private set; }
    public string Number { get; private set; } = "";
    public int CustomerId { get; private set; }
    public Customer Customer { get; private set; } = null!;
    public decimal Balance { get; private set; }
    public DateOnly Opened { get; private set; }
    public AccountStatus Status { get; private set; }
}'''

F["abstr2"] = r'''using BankingApp.Domain.Customers;

namespace BankingApp.Application.Abstractions;

public interface ICustomerRepository
{
    Task<bool> ExistsByEmailAsync(string email, CancellationToken ct);
    Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct);
    Task<Customer?> GetByEmailAsync(string email, CancellationToken ct);
    Task<Customer?> GetByIdWithAccountsAsync(int id, CancellationToken ct);
    Task AddAsync(Customer customer, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}'''

F["register"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Domain.Accounts;
using BankingApp.Domain.Customers;

namespace BankingApp.Application.Handlers.CommandHandlers.Register;

public class RegisterHandler : IHandler<RegisterCommand, RegisterResult>
{
    private readonly ICustomerRepository _customers;
    private readonly IPasswordHasher _hasher;

    public RegisterHandler(ICustomerRepository customers, IPasswordHasher hasher)
    {
        _customers = customers;
        _hasher = hasher;
    }

    public async Task<Response<RegisterResult>> HandleAsync(RegisterCommand request, CancellationToken ct)
    {
        // collect ALL the problems, so the client can fix them in one go
        var errors = new List<Error>();

        if (request.Password.Length < 8)
            errors.Add(Error.Validation("Password must have at least 8 characters."));
        if (await _customers.ExistsByEmailAsync(request.Email.Trim().ToLowerInvariant(), ct))
            errors.Add(Error.Conflict("Email already registered."));
        if (await _customers.ExistsByTaxIdAsync(request.TaxId, ct))
            errors.Add(Error.Conflict($"A customer with tax id {request.TaxId} already exists."));

        if (errors.Count > 0)
            return Response<RegisterResult>.Fail(errors);

        var customer = new Customer(request.Name, request.TaxId, request.Email, _hasher.Hash(request.Password));

        // every customer starts with a first account
        var number = $"AC-{Random.Shared.Next(100000, 999999)}";
        customer.Accounts.Add(Account.Open(number, customer, 0m, DateOnly.FromDateTime(DateTime.Today)));

        await _customers.AddAsync(customer, ct);
        await _customers.SaveChangesAsync(ct);

        return Response<RegisterResult>.Ok(new RegisterResult { CustomerId = customer.Id, AccountNumber = number });
    }
}'''

F["login"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.Login;

public class LoginHandler : IHandler<LoginCommand, LoginResult>
{
    private readonly ICustomerRepository _customers;
    private readonly IPasswordHasher _hasher;
    private readonly ITokenService _tokens;

    public LoginHandler(ICustomerRepository customers, IPasswordHasher hasher, ITokenService tokens)
    {
        _customers = customers;
        _hasher = hasher;
        _tokens = tokens;
    }

    public async Task<Response<LoginResult>> HandleAsync(LoginCommand request, CancellationToken ct)
    {
        var customer = await _customers.GetByEmailAsync(request.Email.Trim().ToLowerInvariant(), ct);

        // same error for "unknown email" and "wrong password": do not reveal which one failed
        if (customer is null || !_hasher.Verify(customer.PasswordHash, request.Password))
            return Response<LoginResult>.Fail(Error.Unauthorized("Invalid email or password."));

        var token = _tokens.Create(customer);
        return Response<LoginResult>.Ok(new LoginResult { AccessToken = token.AccessToken, ExpiresAtUtc = token.ExpiresAtUtc });
    }
}'''

F["dashboard"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Domain.Accounts;

namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class RetrieveDashboardHandler : IHandler<RetrieveDashboardQuery, DashboardResult>
{
    private readonly ICustomerRepository _customers;

    public RetrieveDashboardHandler(ICustomerRepository customers) => _customers = customers;

    public async Task<Response<DashboardResult>> HandleAsync(RetrieveDashboardQuery request, CancellationToken ct)
    {
        var customer = await _customers.GetByIdWithAccountsAsync(request.CustomerId, ct);
        if (customer is null)
            return Response<DashboardResult>.Fail(Error.NotFound("Customer not found."));

        var accounts = customer.Accounts
            .Where(a => a.Status == AccountStatus.Active)
            .OrderBy(a => a.Number)
            .Select(a => new DashboardAccount
            {
                Number = a.Number,
                Balance = a.Balance,
                Status = a.Status.ToString(),
                Opened = a.Opened
            })
            .ToList();

        return Response<DashboardResult>.Ok(new DashboardResult
        {
            CustomerName = customer.Name,
            Email = customer.Email,
            TotalBalance = accounts.Sum(a => a.Balance),
            Accounts = accounts
        });
    }
}'''

F["app_di2"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Handlers.CommandHandlers.Login;
using BankingApp.Application.Handlers.CommandHandlers.Register;
using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IHandler<RegisterCommand, RegisterResult>, RegisterHandler>();
        services.AddScoped<IHandler<LoginCommand, LoginResult>, LoginHandler>();
        services.AddScoped<IHandler<RetrieveDashboardQuery, DashboardResult>, RetrieveDashboardHandler>();
        return services;
    }
}'''

F["jwtopts"] = r'''namespace BankingApp.Infrastructure.Authentication;

public class JwtOptions
{
    public string Issuer { get; set; } = "";
    public string Audience { get; set; } = "";
    public string Key { get; set; } = "";          // comes from appsettings.json
    public int ExpiresMinutes { get; set; } = 60;
}'''

F["jwtsvc"] = r'''using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using BankingApp.Application.Abstractions;
using BankingApp.Domain.Customers;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

namespace BankingApp.Infrastructure.Authentication;

public class JwtTokenService : ITokenService
{
    private readonly JwtOptions _options;

    public JwtTokenService(IOptions<JwtOptions> options) => _options = options.Value;

    public TokenResult Create(Customer customer)
    {
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, customer.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, customer.Email),
            new Claim("name", customer.Name)
        };

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_options.Key));
        var expires = DateTime.UtcNow.AddMinutes(_options.ExpiresMinutes);

        var token = new JwtSecurityToken(
            issuer: _options.Issuer,
            audience: _options.Audience,
            claims: claims,
            expires: expires,
            signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));

        return new TokenResult
        {
            AccessToken = new JwtSecurityTokenHandler().WriteToken(token),
            ExpiresAtUtc = expires
        };
    }
}'''

F["hasher"] = r'''using BankingApp.Application.Abstractions;
using Microsoft.AspNetCore.Identity;

namespace BankingApp.Infrastructure.Authentication;

// uses the hasher from ASP.NET Core Identity (salted, slow on purpose), without the rest of Identity
public class PasswordHasherService : IPasswordHasher
{
    private readonly PasswordHasher<object> _hasher = new();

    public string Hash(string password)
        => _hasher.HashPassword(null!, password);

    public bool Verify(string hash, string password)
        => _hasher.VerifyHashedPassword(null!, hash, password) != PasswordVerificationResult.Failed;
}'''

F["cfg_customer2"] = r'''using BankingApp.Domain.Customers;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace BankingApp.Infrastructure.Persistence.Configurations;

public class CustomerConfiguration : IEntityTypeConfiguration<Customer>
{
    public void Configure(EntityTypeBuilder<Customer> builder)
    {
        builder.Property(c => c.Name).HasMaxLength(100).IsRequired();
        builder.Property(c => c.TaxId).HasMaxLength(9).IsRequired();
        builder.Property(c => c.Email).HasMaxLength(200).IsRequired();
        builder.Property(c => c.PasswordHash).HasMaxLength(500).IsRequired();
        builder.HasIndex(c => c.TaxId).IsUnique();
        builder.HasIndex(c => c.Email).IsUnique();
    }
}'''

F["cfg_account"] = r'''using BankingApp.Domain.Accounts;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace BankingApp.Infrastructure.Persistence.Configurations;

public class AccountConfiguration : IEntityTypeConfiguration<Account>
{
    public void Configure(EntityTypeBuilder<Account> builder)
    {
        builder.Property(a => a.Number).HasMaxLength(20).IsRequired();
        builder.HasIndex(a => a.Number).IsUnique();
        builder.Property(a => a.Balance).HasPrecision(18, 2);
        builder.Property(a => a.Status).HasConversion<string>().HasMaxLength(20);

        builder.HasOne(a => a.Customer)
               .WithMany(c => c.Accounts)
               .HasForeignKey(a => a.CustomerId);
    }
}'''

F["ctx2"] = r'''using BankingApp.Domain.Accounts;
using BankingApp.Domain.Customers;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Persistence;

public class BankingAppContext : DbContext
{
    public BankingAppContext(DbContextOptions<BankingAppContext> options) : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Account> Accounts => Set<Account>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
        => modelBuilder.ApplyConfigurationsFromAssembly(typeof(BankingAppContext).Assembly);
}'''

F["repo2"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Domain.Customers;
using BankingApp.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Repositories;

public class CustomerRepository : ICustomerRepository
{
    private readonly BankingAppContext _db;

    public CustomerRepository(BankingAppContext db) => _db = db;

    public Task<bool> ExistsByEmailAsync(string email, CancellationToken ct)
        => _db.Customers.AnyAsync(c => c.Email == email, ct);

    public Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct)
        => _db.Customers.AnyAsync(c => c.TaxId == taxId, ct);

    public Task<Customer?> GetByEmailAsync(string email, CancellationToken ct)
        => _db.Customers.FirstOrDefaultAsync(c => c.Email == email, ct);

    public Task<Customer?> GetByIdWithAccountsAsync(int id, CancellationToken ct)
        => _db.Customers.Include(c => c.Accounts)
                        .AsNoTracking()
                        .FirstOrDefaultAsync(c => c.Id == id, ct);

    public async Task AddAsync(Customer customer, CancellationToken ct)
        => await _db.Customers.AddAsync(customer, ct);

    public Task SaveChangesAsync(CancellationToken ct)
        => _db.SaveChangesAsync(ct);
}'''

F["infra_di2"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Infrastructure.Authentication;
using BankingApp.Infrastructure.Persistence;
using BankingApp.Infrastructure.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<BankingAppContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("BankingApp")));

        services.Configure<JwtOptions>(configuration.GetSection("Jwt"));

        services.AddScoped<ICustomerRepository, CustomerRepository>();
        services.AddSingleton<IPasswordHasher, PasswordHasherService>();
        services.AddScoped<ITokenService, JwtTokenService>();
        return services;
    }
}'''

F["mig2"] = r'''# if you created test customers in step 1, start clean (they have no email):
dotnet ef database drop -f -p src/BankingApp.Infrastructure -s src/BankingApp.Api

dotnet ef migrations add AddCredentialsAndAccounts -p src/BankingApp.Infrastructure -s src/BankingApp.Api -o Persistence/Migrations
dotnet ef database update                          -p src/BankingApp.Infrastructure -s src/BankingApp.Api'''

F["contracts2"] = r'''using System.ComponentModel.DataAnnotations;

namespace BankingApp.Api.Contracts.Auth;

public class RegisterRequest
{
    [Required, StringLength(100)]
    public string Name { get; set; } = "";

    [Required, RegularExpression(@"^\d{9}$")]
    public string TaxId { get; set; } = "";

    [Required, EmailAddress]
    public string Email { get; set; } = "";

    [Required, MinLength(8)]
    public string Password { get; set; } = "";
}'''

F["ctrl_auth"] = r'''using BankingApp.Api.Contracts.Auth;
using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.CommandHandlers.Login;
using BankingApp.Application.Handlers.CommandHandlers.Register;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Controllers;

[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly IHandler<RegisterCommand, RegisterResult> _register;
    private readonly IHandler<LoginCommand, LoginResult> _login;

    public AuthController(
        IHandler<RegisterCommand, RegisterResult> register,
        IHandler<LoginCommand, LoginResult> login)
    {
        _register = register;
        _login = login;
    }

    [AllowAnonymous]
    [HttpPost("register")]
    public async Task<Response<RegisterResponse>> Register(RegisterRequest body, CancellationToken ct)
    {
        var result = await _register.HandleAsync(
            new RegisterCommand { Name = body.Name, TaxId = body.TaxId, Email = body.Email, Password = body.Password }, ct);

        return result.Map(RegisterResponse.From);
    }

    [AllowAnonymous]
    [HttpPost("login")]
    public async Task<Response<LoginResponse>> Login(LoginRequest body, CancellationToken ct)
    {
        var result = await _login.HandleAsync(new LoginCommand { Email = body.Email, Password = body.Password }, ct);
        return result.Map(LoginResponse.From);
    }
}'''

F["ctrl_dash"] = r'''using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using BankingApp.Api.Contracts.Dashboard;
using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Controllers;

[ApiController]
[Route("api/dashboard")]
[Authorize]                                   // every method here requires a valid token
public class DashboardController : ControllerBase
{
    private readonly IHandler<RetrieveDashboardQuery, DashboardResult> _handler;

    public DashboardController(IHandler<RetrieveDashboardQuery, DashboardResult> handler) => _handler = handler;

    [HttpPost("retrieve")]
    public async Task<Response<DashboardResponse>> RetrieveDashboard(CancellationToken ct)
    {
        // the customer id comes from the token, never from the request
        var customerId = int.Parse(User.FindFirstValue(JwtRegisteredClaimNames.Sub)!);

        var result = await _handler.HandleAsync(new RetrieveDashboardQuery { CustomerId = customerId }, ct);
        return result.Map(DashboardResponse.From);
    }
}'''

F["rpc_events"] = r'''using BankingApp.Application.Common;
using Microsoft.AspNetCore.Authentication.JwtBearer;

namespace BankingApp.Api.Authentication;

// RPC: even "no token" and "no permission" answer 200, with the error in the body
public class RpcJwtBearerEvents : JwtBearerEvents
{
    public RpcJwtBearerEvents()
    {
        OnChallenge = context =>
        {
            context.HandleResponse();               // skip the default 401
            return Write(context.HttpContext, Error.Unauthorized("Missing or invalid token."));
        };

        OnForbidden = context =>
            Write(context.HttpContext, Error.Forbidden("You do not have permission for this operation."));
    }

    private static Task Write(HttpContext http, Error error)
    {
        http.Response.StatusCode = StatusCodes.Status200OK;
        return http.Response.WriteAsJsonAsync(Response<object>.Fail(error));
    }
}'''

F["program2"] = r'''using System.Text;
using BankingApp.Api.Authentication;
using BankingApp.Api.Middleware;
using BankingApp.Api.Responses;
using BankingApp.Application;
using BankingApp.Infrastructure;
using BankingApp.Infrastructure.Authentication;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers()
    .ConfigureApiBehaviorOptions(o =>
        o.InvalidModelStateResponseFactory = ValidationResponse.Create);
builder.Services.AddOpenApi();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

// JWT bearer: the API validates the token that the client sends in the Authorization header
var jwt = builder.Configuration.GetSection("Jwt").Get<JwtOptions>()
          ?? throw new InvalidOperationException("Missing Jwt configuration.");

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Events = new RpcJwtBearerEvents();   // 401/403 become 200 + error
        options.MapInboundClaims = false;    // keep the claim called "sub" as "sub"
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = jwt.Issuer,
            ValidateAudience = true,
            ValidAudience = jwt.Audience,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwt.Key)),
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });
builder.Services.AddAuthorization();

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseSwaggerUI(o => o.SwaggerEndpoint("/openapi/v1.json", "v1"));
}

app.UseHttpsRedirection();
app.UseAuthentication();                     // 1. who are you? (reads the token)
app.UseAuthorization();                      // 2. can you do this? ([Authorize])
app.MapControllers();

app.Run();'''

F["jwt_decoded"] = r'''# header
{ "alg": "HS256", "typ": "JWT" }

# payload (the claims)
{
  "sub": "1",
  "email": "ana@example.com",
  "name": "Ana Pereira",
  "exp": 1793700000,
  "iss": "BankingApp",
  "aud": "BankingApp.Clients"
}

# signature = HMACSHA256(header + "." + payload, Jwt:Key)
# anyone can READ the payload (base64): never put secrets in it'''

# ---- Bruno files
F["bru_json"] = r'''{
  "version": "1",
  "name": "BankingApp",
  "type": "collection"
}'''
F["bru_env"] = r'''vars {
  baseUrl: https://localhost:5001
}'''
F["bru_register"] = r'''meta {
  name: Register
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/api/auth/register
  body: json
  auth: none
}

body:json {
  {
    "name": "Ana Pereira",
    "taxId": "123456789",
    "email": "ana@example.com",
    "password": "Passw0rd!"
  }
}'''
F["bru_login"] = r'''meta {
  name: Login
  type: http
  seq: 2
}

post {
  url: {{baseUrl}}/api/auth/login
  body: json
  auth: none
}

body:json {
  {
    "email": "ana@example.com",
    "password": "Passw0rd!"
  }
}

vars:post-response {
  token: res.body.data.accessToken
}'''
F["bru_dash"] = r'''meta {
  name: RetrieveDashboard
  type: http
  seq: 3
}

post {
  url: {{baseUrl}}/api/dashboard/retrieve
  body: json
  auth: bearer
}

body:json {
  {}
}

auth:bearer {
  token: {{token}}
}'''
F["tests2"] = r'''using BankingApp.Application.Abstractions;
using BankingApp.Application.Handlers.CommandHandlers.Login;
using BankingApp.Domain.Customers;
using NSubstitute;

namespace BankingApp.Tests.Application;

public class LoginHandlerTests
{
    private readonly ICustomerRepository _customers = Substitute.For<ICustomerRepository>();
    private readonly IPasswordHasher _hasher = Substitute.For<IPasswordHasher>();
    private readonly ITokenService _tokens = Substitute.For<ITokenService>();
    private readonly LoginHandler _handler;

    public LoginHandlerTests()
        => _handler = new LoginHandler(_customers, _hasher, _tokens);

    [Fact]
    public async Task HandleAsync_WrongPassword_ReturnsUnauthorizedError()
    {
        var customer = new Customer("Ana Pereira", "123456789", "ana@example.com", "hash");
        _customers.GetByEmailAsync("ana@example.com", Arg.Any<CancellationToken>()).Returns(customer);
        _hasher.Verify("hash", "wrong").Returns(false);

        var response = await _handler.HandleAsync(new LoginCommand { Email = "ana@example.com", Password = "wrong" }, CancellationToken.None);

        Assert.False(response.Success);
        Assert.Equal("unauthorized", Assert.Single(response.Errors).Code);
        _tokens.DidNotReceive().Create(Arg.Any<Customer>());
    }

    [Fact]
    public async Task HandleAsync_ValidCredentials_ReturnsToken()
    {
        var customer = new Customer("Ana Pereira", "123456789", "ana@example.com", "hash");
        _customers.GetByEmailAsync("ana@example.com", Arg.Any<CancellationToken>()).Returns(customer);
        _hasher.Verify("hash", "Passw0rd!").Returns(true);
        _tokens.Create(customer).Returns(new TokenResult { AccessToken = "token-value", ExpiresAtUtc = DateTime.UtcNow.AddHours(1) });

        var response = await _handler.HandleAsync(new LoginCommand { Email = "ana@example.com", Password = "Passw0rd!" }, CancellationToken.None);

        Assert.True(response.Success);
        Assert.Equal("token-value", response.Data!.AccessToken);
    }
}'''

# ============================================================ TREES
def d(n, desc, *c): return {'n': n, 'd': desc, 'c': list(c)}
def f(n, desc, fid=None, tag=None): return {'n': n, 'd': desc, 'f': fid, 'tag': tag}

TREE1 = d('BankingApp/', 'Pasta raiz do repositório. Tem a solução e duas pastas: src (código) e tests (testes).',
  f('BankingApp.sln', 'A solução. Só lista os cinco projetos, para o IDE os abrir em conjunto.'),
  d('src/', 'Todo o código que vai para produção.',
    d('BankingApp.Domain/', 'Camada 1, o centro. Regras do negócio. Não referencia nada.',
      d('Common/', 'Tipos partilhados por todo o Domain.', f('DomainException.cs', 'Exceção base das regras do negócio. O ExceptionMiddleware converte-a num erro validation.', 'BankingApp.Domain/Common/DomainException.cs')),
      d('Customers/', 'Tudo o que diz respeito a clientes.', f('Customer.cs', 'A primeira entidade. Valida nome e NIF na criação; setters privados.', 'BankingApp.Domain/Customers/Customer.cs'))),
    d('BankingApp.Application/', 'Camada 2. Casos de uso e contratos. Só referencia o Domain.',
      d('Abstractions/', 'Interfaces que a Application precisa mas não implementa.',
        f('IHandler.cs', 'O contrato de todos os casos de uso: Request entra, Response sai.', 'BankingApp.Application/Abstractions/IHandler.cs'),
        f('ICustomerRepository.cs', 'O contrato do repositório. A implementação vive na Infrastructure.', 'BankingApp.Application/Abstractions/ICustomerRepository.cs')),
      d('Common/', 'A abstração de entrada e de saída (a base da API RPC).',
        f('Request.cs', 'Classe base de todos os comandos e consultas.', 'BankingApp.Application/Common/Request.cs'),
        f('Response.cs', 'Response<T>: success, errors e data.', 'BankingApp.Application/Common/Response.cs'),
        f('Empty.cs', 'Os dados de um caso de uso que não devolve nada.', 'BankingApp.Application/Common/Empty.cs'),
        f('Error.cs', 'Um erro: código e mensagem, com uma fábrica por tipo.', 'BankingApp.Application/Common/Error.cs')),
      d('Handlers/', 'Os casos de uso, separados em comandos (alteram dados) e consultas (só leem).',
      d('CommandHandlers/', 'Um caso de uso por pasta, com tudo o que lhe diz respeito: comando, resultado e handler.',
        d('CreateCustomer/', 'O caso de uso CreateCustomer.',
          f('CreateCustomerCommand.cs', 'Os dados de entrada de CreateCustomer.', 'BankingApp.Application/Handlers/CommandHandlers/CreateCustomer/CreateCustomerCommand.cs'),
          f('CustomerResult.cs', 'O resultado: um cliente.', 'BankingApp.Application/Handlers/CommandHandlers/CreateCustomer/CustomerResult.cs'),
          f('CreateCustomerHandler.cs', 'O caso de uso CreateCustomer.', 'BankingApp.Application/Handlers/CommandHandlers/CreateCustomer/CreateCustomerHandler.cs'))),
      d('QueryHandlers/', 'O mesmo para as consultas, que só leem dados.',
        d('ListCustomers/', 'O caso de uso ListCustomers.',
          f('ListCustomersQuery.cs', 'A consulta ListCustomers.', 'BankingApp.Application/Handlers/QueryHandlers/ListCustomers/ListCustomersQuery.cs'),
          f('ListCustomersHandler.cs', 'O caso de uso ListCustomers.', 'BankingApp.Application/Handlers/QueryHandlers/ListCustomers/ListCustomersHandler.cs')))),
      f('DependencyInjection.cs', 'AddApplication(): regista os handlers no container.', 'BankingApp.Application/DependencyInjection.cs')),
    d('BankingApp.Infrastructure/', 'Camada 3. Detalhes técnicos: EF Core e base de dados. Referencia a Application.',
      d('Persistence/', 'Tudo o que é EF Core.',
        f('BankingAppContext.cs', 'O DbContext. Um DbSet por tabela.', 'BankingApp.Infrastructure/Persistence/BankingAppContext.cs'),
        d('Configurations/', 'Uma classe IEntityTypeConfiguration por entidade (Fluent API).', f('CustomerConfiguration.cs', 'Tamanhos, obrigatoriedade e índice único do NIF.', 'BankingApp.Infrastructure/Persistence/Configurations/CustomerConfiguration.cs')),
        d('Migrations/', 'Gerada pelo comando dotnet ef. Não se escreve à mão: revê-se.', f('(ficheiros gerados)', 'InitialCreate, o snapshot do modelo e o Designer.'))),
      d('Repositories/', 'Implementações dos contratos da Application.', f('CustomerRepository.cs', 'Implementa ICustomerRepository com o EF Core.', 'BankingApp.Infrastructure/Repositories/CustomerRepository.cs')),
      f('DependencyInjection.cs', 'AddInfrastructure(): DbContext, connection string e repositórios.', 'BankingApp.Infrastructure/DependencyInjection.cs')),
    d('BankingApp.Api/', 'Camada 4. HTTP. Referencia a Application e a Infrastructure (só para a registar).',
      d('Contracts/', 'DTOs: o formato dos pedidos e das respostas.', d('Customers/', 'Contratos dos endpoints de clientes.', f('NewCustomer.cs', 'O pedido, com validação.', 'BankingApp.Api/Contracts/Customers/NewCustomer.cs'), f('CustomerResponse.cs', 'A resposta.', 'BankingApp.Api/Contracts/Customers/CustomerResponse.cs'))),
      d('Controllers/', 'Um controller por recurso.', f('CustomersController.cs', 'Operações de clientes (create e list), todas POST. Converte o pedido num comando e devolve um Response.', 'BankingApp.Api/Controllers/CustomersController.cs')),
      d('Responses/', 'Respostas fora do controller.', f('ValidationResponse.cs', 'DTO inválido: responde 200 com a lista de erros.', 'BankingApp.Api/Responses/ValidationResponse.cs')),
      d('Middleware/', 'Componentes do pipeline.', f('ExceptionMiddleware.cs', 'Converte exceções em Response com erro, sempre com HTTP 200.', 'BankingApp.Api/Middleware/ExceptionMiddleware.cs')),
      d('Properties/', 'Gerada pelo template.', f('launchSettings.json', 'Portas e URL de arranque. Põe "launchUrl": "swagger".', 'BankingApp.Api/Properties/launchSettings.json')),
      f('appsettings.json', 'Configuração: connection string e logging.', 'BankingApp.Api/appsettings.json'),
      f('Program.cs', 'Ponto de entrada: serviços, pipeline e Swagger UI.', 'BankingApp.Api/Program.cs'))),
  d('tests/', 'Projetos de teste.',
    d('BankingApp.Tests/', 'xUnit. Referencia o Domain e a Application.', d('Domain/', 'Testes às regras do Domain.', f('CustomerTests.cs', 'O primeiro teste: valida o NIF e o nome.', 'BankingApp.Tests/Domain/CustomerTests.cs')),
      d('Application/', 'Testes à Application.', f('ResponseTests.cs', 'Testa o Response: Ok, Fail e Map.', 'BankingApp.Tests/Application/ResponseTests.cs')))))

TREE2 = d('BankingApp/', 'Só aparecem as pastas e ficheiros que mudam neste passo.',
  d('src/', 'Código.',
    d('BankingApp.Domain/', 'Ganha a entidade Account e as credenciais no Customer.',
      d('Accounts/', 'Contas bancárias.', f('Account.cs', 'Entidade Account e Account.Open.', 'BankingApp.Domain/Accounts/Account.cs', 'novo'), f('AccountStatus.cs', 'O estado da conta: Active ou Closed.', 'BankingApp.Domain/Accounts/AccountStatus.cs', 'novo')),
      d('Customers/', 'Clientes.', f('Customer.cs', 'Passa a ter Email, PasswordHash e a lista de contas.', 'BankingApp.Domain/Customers/Customer.cs', 'alterado'))),
    d('BankingApp.Application/', 'Casos de uso de autenticação e dashboard.',
      d('Abstractions/', 'Contratos.', f('ICustomerRepository.cs', 'Ganha os métodos de email e de leitura com contas.', 'BankingApp.Application/Abstractions/ICustomerRepository.cs', 'alterado'), f('IPasswordHasher.cs', 'Contrato do hash das passwords.', 'BankingApp.Application/Abstractions/IPasswordHasher.cs', 'novo'), f('ITokenService.cs', 'Contrato que cria o token.', 'BankingApp.Application/Abstractions/ITokenService.cs', 'novo'), f('TokenResult.cs', 'O token e a data de expiração.', 'BankingApp.Application/Abstractions/TokenResult.cs', 'novo')),
      d('Handlers/', 'Os casos de uso, separados em comandos e consultas.',
      d('CommandHandlers/', 'Um caso de uso por pasta. Entram o Register e o Login; sai o CreateCustomer.',
        d('Register/', 'Caso de uso anónimo.', f('RegisterCommand.cs', 'Os dados de entrada do Register.', 'BankingApp.Application/Handlers/CommandHandlers/Register/RegisterCommand.cs', 'novo'), f('RegisterResult.cs', 'O resultado: id do cliente e número da conta.', 'BankingApp.Application/Handlers/CommandHandlers/Register/RegisterResult.cs', 'novo'), f('RegisterHandler.cs', 'Cria o cliente e a primeira conta.', 'BankingApp.Application/Handlers/CommandHandlers/Register/RegisterHandler.cs', 'novo')),
        d('Login/', 'Caso de uso anónimo.', f('LoginCommand.cs', 'Os dados de entrada do Login.', 'BankingApp.Application/Handlers/CommandHandlers/Login/LoginCommand.cs', 'novo'), f('LoginResult.cs', 'O resultado: o token.', 'BankingApp.Application/Handlers/CommandHandlers/Login/LoginResult.cs', 'novo'), f('LoginHandler.cs', 'Valida as credenciais e devolve o token.', 'BankingApp.Application/Handlers/CommandHandlers/Login/LoginHandler.cs', 'novo')),
        d('CreateCustomer/', 'Apaga esta pasta: serviu só para validar o Passo 1.', f('(apagar)', 'CreateCustomerCommand, CustomerResult e CreateCustomerHandler.', None, 'apagar'))),
      d('QueryHandlers/', 'Entra o RetrieveDashboard; sai o ListCustomers.',
        d('RetrieveDashboard/', 'Caso de uso autenticado.', f('RetrieveDashboardQuery.cs', 'A consulta: o id do cliente.', 'BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/RetrieveDashboardQuery.cs', 'novo'), f('DashboardAccount.cs', 'Uma conta no resumo.', 'BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/DashboardAccount.cs', 'novo'), f('DashboardResult.cs', 'O resumo: cliente, saldo total e contas.', 'BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/DashboardResult.cs', 'novo'), f('RetrieveDashboardHandler.cs', 'Calcula o resumo das contas ativas.', 'BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/RetrieveDashboardHandler.cs', 'novo')),
        d('ListCustomers/', 'Apaga esta pasta: serviu só para validar o Passo 1.', f('(apagar)', 'ListCustomersQuery e ListCustomersHandler.', None, 'apagar'))))),
    d('BankingApp.Infrastructure/', 'Implementa o token, o hash e as novas tabelas.',
      d('Authentication/', 'Tudo o que é segurança.', f('JwtOptions.cs', 'As opções lidas da secção "Jwt".', 'BankingApp.Infrastructure/Authentication/JwtOptions.cs', 'novo'), f('JwtTokenService.cs', 'Cria e assina o token.', 'BankingApp.Infrastructure/Authentication/JwtTokenService.cs', 'novo'), f('PasswordHasherService.cs', 'Faz o hash e a verificação das passwords.', 'BankingApp.Infrastructure/Authentication/PasswordHasherService.cs', 'novo')),
      d('Persistence/', 'EF Core.', f('BankingAppContext.cs', 'Ganha DbSet<Account>.', 'BankingApp.Infrastructure/Persistence/BankingAppContext.cs', 'alterado'), d('Configurations/', 'Fluent API.', f('CustomerConfiguration.cs', 'Email e PasswordHash.', 'BankingApp.Infrastructure/Persistence/Configurations/CustomerConfiguration.cs', 'alterado'), f('AccountConfiguration.cs', 'Número único, precisão e relação.', 'BankingApp.Infrastructure/Persistence/Configurations/AccountConfiguration.cs', 'novo'))),
      d('Repositories/', 'Implementações.', f('CustomerRepository.cs', 'Novos métodos de leitura.', 'BankingApp.Infrastructure/Repositories/CustomerRepository.cs', 'alterado')),
      f('DependencyInjection.cs', 'Regista JwtOptions, hasher e token service.', 'BankingApp.Infrastructure/DependencyInjection.cs', 'alterado')),
    d('BankingApp.Api/', 'Autenticação e novos controllers.',
      d('Contracts/', 'DTOs.', d('Auth/', 'Register e Login.', f('RegisterRequest.cs', 'O pedido de Register, com validação.', 'BankingApp.Api/Contracts/Auth/RegisterRequest.cs', 'novo'), f('RegisterResponse.cs', 'A resposta de Register.', 'BankingApp.Api/Contracts/Auth/RegisterResponse.cs', 'novo'), f('LoginRequest.cs', 'O pedido de Login.', 'BankingApp.Api/Contracts/Auth/LoginRequest.cs', 'novo'), f('LoginResponse.cs', 'A resposta de Login, com o token.', 'BankingApp.Api/Contracts/Auth/LoginResponse.cs', 'novo')), d('Dashboard/', 'RetrieveDashboard.', f('DashboardAccountResponse.cs', 'Uma conta na resposta.', 'BankingApp.Api/Contracts/Dashboard/DashboardAccountResponse.cs', 'novo'), f('DashboardResponse.cs', 'A resposta do dashboard.', 'BankingApp.Api/Contracts/Dashboard/DashboardResponse.cs', 'novo'))),
      d('Controllers/', 'Controllers.', f('AuthController.cs', 'Register e Login (anónimos).', 'BankingApp.Api/Controllers/AuthController.cs', 'novo'), f('DashboardController.cs', 'RetrieveDashboard (autenticado).', 'BankingApp.Api/Controllers/DashboardController.cs', 'novo'), f('CustomersController.cs', 'Apaga: foi só para validar o Passo 1.', None, 'apagar')),
      d('Authentication/', 'Respostas de autenticação.', f('RpcJwtBearerEvents.cs', 'Sem token ou sem permissão: 200 com o erro unauthorized ou forbidden.', 'BankingApp.Api/Authentication/RpcJwtBearerEvents.cs', 'novo')),
      f('appsettings.json', 'Ganha a secção "Jwt", com a chave de desenvolvimento.', 'BankingApp.Api/appsettings.json', 'alterado'),
      f('Program.cs', 'Autenticação JWT (com os eventos RPC) e UseAuthentication/UseAuthorization.', 'BankingApp.Api/Program.cs', 'alterado'))),
  d('tests/', 'Testes.', d('BankingApp.Tests/', 'xUnit.', d('Application/', 'Testes aos handlers.', f('LoginHandlerTests.cs', 'Dois testes com mocks.', 'BankingApp.Tests/Application/LoginHandlerTests.cs', 'novo')))))


# ============================================================ PHASES
SEC1 = [
 dict(t="Criar a solução, os projetos e as referências", intro="Convenção do projeto inteiro: tudo são classes (sem records), uma classe por ficheiro, e cada classe com uma única responsabilidade. A solução e os projetos criam-se no IDE (Visual Studio ou Rider), sem linha de comandos. As referências entre projetos são a arquitetura: se o Domain não referencia nada, ninguém o consegue contaminar com EF Core. Os únicos comandos deste passo instalam dependências.",
      steps=["Criar a solução BankingApp, com as pastas src e tests", "Criar os cinco projetos: Domain, Application e Infrastructure (Class Library), Api (ASP.NET Core Web API com controllers, .NET 10) e Tests (xUnit)", "Configurar as Project References segundo a regra das dependências", "Apagar os ficheiros de exemplo dos templates (Class1, WeatherForecast e UnitTest1)", "Instalar os pacotes NuGet, a UI do Swagger e a ferramenta dotnet-ef", "Compilar a solução (Build Solution)"],
      files=[dict(name="Project References", lang="txt", code=F["s1_mkdir"]), dict(name="Instalar dependências", lang="sh", code=F["s1_sh"])],
      check="Build succeeded.\n    0 Warning(s)\n    0 Error(s)"),
 dict(t="Domain: a primeira entidade", intro="Customer é a primeira entidade. A validação vive dentro da própria classe, e os setters são privados para o estado só mudar por métodos da classe.",
      files=[dict(name="BankingApp.Domain/Common/DomainException.cs", lang="cs", code=F["domain_exc"]), dict(name="BankingApp.Domain/Customers/Customer.cs", lang="cs", code=F["customer1"])]),
 dict(t="Application: a abstração de entrada e de saída (API RPC)", intro="Esta API é RPC: o HTTP é só o transporte. Todos os pedidos são POST, para /api/<área>/<ação> (por exemplo, /api/accounts/deposit), e os parâmetros vão sempre no corpo JSON, nunca na rota nem na query string. Se o pedido chegou ao servidor e foi processado, a resposta é sempre 200 OK, e o resultado vem no corpo. Para isso, todos os casos de uso recebem um Request e devolvem um Response, que tem uma lista de erros. Quem chama lê success e errors em vez do código HTTP. Criamos já estas peças, porque tudo o que vem a seguir as usa.",
      steps=["Criar o Error, com uma fábrica por tipo (validation, not_found, conflict, unauthorized, forbidden)", "Criar a classe base Request, de onde herdam todos os comandos e consultas", "Criar o Response<T>: success é «não há erros»; Data guarda o resultado; Empty é para os casos de uso sem dados", "Criar o IHandler<TRequest, TData>, o contrato de qualquer caso de uso"],
      files=[dict(name="BankingApp.Application/Common/Error.cs", lang="cs", code=F["app_exc"]), dict(name="BankingApp.Application/Common/Request.cs", lang="cs", code=F["resp_request"]), dict(name="BankingApp.Application/Common/Response.cs", lang="cs", code=F["resp_response"]), dict(name="BankingApp.Application/Common/Empty.cs", lang="cs", code=F["resp_empty"]), dict(name="BankingApp.Application/Abstractions/IHandler.cs", lang="cs", code=F["resp_handler"])]),
 dict(t="Application: contratos e o primeiro caso de uso", intro="A Application define o que precisa (ICustomerRepository) e escreve cada caso de uso em três classes pequenas, cada uma no seu ficheiro: ficam todas juntas na pasta do caso de uso, dentro de Handlers/CommandHandlers (comandos) ou de Handlers/QueryHandlers (consultas), por exemplo Handlers/CommandHandlers/CreateCustomer. A pasta Handlers agrupa os dois. Um handler recebe um Request e devolve um Response: os erros de negócio devolvem-se, não se lançam. Não sabe nada de EF Core nem de HTTP.",
      files=[dict(name="BankingApp.Application/Abstractions/ICustomerRepository.cs", lang="cs", code=F["repo_if1"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/CreateCustomer/CreateCustomerCommand.cs", lang="cs", code=F["cust_command"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/CreateCustomer/CustomerResult.cs", lang="cs", code=F["cust_result"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/CreateCustomer/CreateCustomerHandler.cs", lang="cs", code=F["create_customer"]), dict(name="BankingApp.Application/Handlers/QueryHandlers/ListCustomers/ListCustomersQuery.cs", lang="cs", code=F["list_query"]), dict(name="BankingApp.Application/Handlers/QueryHandlers/ListCustomers/ListCustomersHandler.cs", lang="cs", code=F["list_customers"]), dict(name="BankingApp.Application/DependencyInjection.cs", lang="cs", code=F["app_di1"])]),
 dict(t="Infrastructure: Entity Framework Core, repositório e ligação à base de dados", intro="O DbContext, a configuração da entidade com a Fluent API, o repositório que implementa o contrato da Application e a connection string. No fim, a primeira migration cria a base de dados.",
      steps=["Criar o BankingAppContext e a CustomerConfiguration", "Implementar o CustomerRepository", "Criar AddInfrastructure() com o DbContext e o repositório", "Pôr a connection string no appsettings.json da Api", "Criar a migration InitialCreate e aplicá-la"],
      files=[dict(name="BankingApp.Infrastructure/Persistence/BankingAppContext.cs", lang="cs", code=F["ctx1"]), dict(name="BankingApp.Infrastructure/Persistence/Configurations/CustomerConfiguration.cs", lang="cs", code=F["cfg_customer1"]), dict(name="BankingApp.Infrastructure/Repositories/CustomerRepository.cs", lang="cs", code=F["repo1"]), dict(name="BankingApp.Infrastructure/DependencyInjection.cs", lang="cs", code=F["infra_di1"]), dict(name="BankingApp.Api/appsettings.json", lang="json", code=F["settings1"]), dict(name="Terminal (migrations)", lang="sh", code=F["mig1"])],
      check="Applying migration '20261103100000_InitialCreate'.\nDone."),
 dict(t="Api: controller, DTOs, tratamento de erros e Swagger", intro="O controller só converte o pedido num comando e devolve o Response do handler. Há três caminhos para um erro, e os três acabam em 200 com a lista de errors: o handler devolve-o, o ValidationResponse apanha os DTOs inválidos, e o ExceptionMiddleware apanha as exceções. O Swagger UI fica disponível em /swagger, em desenvolvimento.",
      steps=["Criar os DTOs com validação", "Criar o CustomersController", "Criar o ValidationResponse", "Criar o ExceptionMiddleware", "Montar o Program.cs com o OpenAPI e o Swagger UI", "Em Properties/launchSettings.json, pôr o launchUrl a swagger"],
      files=[dict(name="BankingApp.Api/Contracts/Customers/NewCustomer.cs", lang="cs", code=F["contracts1"]), dict(name="BankingApp.Api/Contracts/Customers/CustomerResponse.cs", lang="cs", code=F["contracts1b"]), dict(name="BankingApp.Api/Controllers/CustomersController.cs", lang="cs", code=F["ctrl_customers"]), dict(name="BankingApp.Api/Responses/ValidationResponse.cs", lang="cs", code=F["validation_resp"]), dict(name="BankingApp.Api/Middleware/ExceptionMiddleware.cs", lang="cs", code=F["mw1"]), dict(name="BankingApp.Api/Program.cs", lang="cs", code=F["program1"]), dict(name="BankingApp.Api/Properties/launchSettings.json", lang="json", code=F["launch"])]),
 dict(t="Testes: os primeiros testes", intro="O projeto de testes já existe. Escreve-se o primeiro teste ao Domain para ficar o padrão (Theory para os casos inválidos, Fact para o caso feliz) e os testes ao Response, que é a peça de que tudo depende.",
      files=[dict(name="BankingApp.Tests/Domain/CustomerTests.cs", lang="cs", code=F["tests1"]), dict(name="BankingApp.Tests/Application/ResponseTests.cs", lang="cs", code=F["tests_resp"])],
      check="Test Explorer\n7 passed, 0 failed, 0 skipped"),
 dict(t="Correr e verificar", intro="A aplicação está funcional quando consegues criar e listar clientes pelo Swagger UI e ver a linha na base de dados. Repara que todas as respostas são 200: o que muda é o corpo.",
      steps=["Correr a BankingApp.Api no IDE (F5) e abrir /swagger", "POST /api/customers/create com um cliente válido: 200 com success true", "Repetir o POST: 200 com success false e o erro conflict", "POST com NIF \"123\": 200 com success false e o erro validation", "POST /api/customers/list e confirmar a linha na tabela Customers (cliente SQL)"],
      files=[dict(name="Pedido de exemplo", lang="http", code=F["http1"])],
      check="HTTP 200  success: true   (cliente criado)\nHTTP 200  success: false  errors: conflict    (NIF repetido)\nHTTP 200  success: false  errors: validation  (NIF inválido)\nHTTP 200  success: true   (lista com 1 cliente)"),
]

SEC2 = [
 dict(t="Como funciona o token JWT", intro="No login, a API devolve um token assinado. O cliente envia-o em cada pedido, no cabeçalho Authorization. A API valida a assinatura e a validade, e fica a saber quem fez o pedido sem ir à base de dados.",
      files=[dict(name="Um JWT descodificado", lang="sh", code=F["jwt_decoded"])]),
 dict(t="Pacotes e configuração do JWT", intro="O token é assinado com uma chave que fica no appsettings.json, na secção Jwt. Para a formação, é a forma mais simples: uma chave de desenvolvimento, que muda de cada vez que quiseres. Num projeto real, esta chave seria um segredo fora do repositório (variável de ambiente ou cofre), mas isso fica para outro dia.",
      steps=["Instalar os pacotes do JWT e do hash de passwords", "Acrescentar a secção Jwt ao appsettings.json, com a Key (pelo menos 32 caracteres)"],
      files=[dict(name="Instalar dependências", lang="sh", code=F["s2_pk"]), dict(name="BankingApp.Api/appsettings.json", lang="json", code=F["settings2"])]),
 dict(t="Domain: credenciais no cliente e a entidade Account", intro="O Customer passa a ter email e hash da password (nunca a password). Cada cliente começa com uma conta, por isso nasce a entidade Account.",
      files=[dict(name="BankingApp.Domain/Customers/Customer.cs", lang="cs", code=F["customer2"]), dict(name="BankingApp.Domain/Accounts/Account.cs", lang="cs", code=F["account"]), dict(name="BankingApp.Domain/Accounts/AccountStatus.cs", lang="cs", code=F["account_status"])]),
 dict(t="Application: Register, Login e RetrieveDashboard", intro="Dois casos de uso anónimos e um autenticado, todos com Request e Response. O Login devolve sempre o mesmo erro (unauthorized) para email desconhecido e password errada, para não revelar que emails existem. O Register junta todos os problemas numa lista de erros.",
      steps=["Acrescentar ao Abstractions o IPasswordHasher, o ITokenService e o TokenResult (um ficheiro cada)", "Criar uma pasta por caso de uso: Handlers/CommandHandlers/Register, Handlers/CommandHandlers/Login e Handlers/QueryHandlers/RetrieveDashboard, com o comando (ou consulta), o resultado e o handler lado a lado", "Registar os handlers no AddApplication()", "Apagar as pastas Handlers/CommandHandlers/CreateCustomer e Handlers/QueryHandlers/ListCustomers, que já não são precisas"],
      files=[dict(name="BankingApp.Application/Abstractions/ICustomerRepository.cs", lang="cs", code=F["abstr2"]), dict(name="BankingApp.Application/Abstractions/IPasswordHasher.cs", lang="cs", code=F["hasher_if"]), dict(name="BankingApp.Application/Abstractions/TokenResult.cs", lang="cs", code=F["token_result"]), dict(name="BankingApp.Application/Abstractions/ITokenService.cs", lang="cs", code=F["token_if"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/Register/RegisterCommand.cs", lang="cs", code=F["reg_command"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/Register/RegisterResult.cs", lang="cs", code=F["reg_result"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/Register/RegisterHandler.cs", lang="cs", code=F["register"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/Login/LoginCommand.cs", lang="cs", code=F["login_command"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/Login/LoginResult.cs", lang="cs", code=F["login_result"]), dict(name="BankingApp.Application/Handlers/CommandHandlers/Login/LoginHandler.cs", lang="cs", code=F["login"]), dict(name="BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/RetrieveDashboardQuery.cs", lang="cs", code=F["dash_query"]), dict(name="BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/DashboardAccount.cs", lang="cs", code=F["dash_account"]), dict(name="BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/DashboardResult.cs", lang="cs", code=F["dash_result"]), dict(name="BankingApp.Application/Handlers/QueryHandlers/RetrieveDashboard/RetrieveDashboardHandler.cs", lang="cs", code=F["dashboard"]), dict(name="BankingApp.Application/DependencyInjection.cs", lang="cs", code=F["app_di2"])]),
 dict(t="Infrastructure: token, hash, tabelas e migration", intro="As implementações dos contratos novos, a configuração da tabela Accounts e a migration que acrescenta as colunas e a tabela.",
      files=[dict(name="BankingApp.Infrastructure/Authentication/JwtOptions.cs", lang="cs", code=F["jwtopts"]), dict(name="BankingApp.Infrastructure/Authentication/JwtTokenService.cs", lang="cs", code=F["jwtsvc"]), dict(name="BankingApp.Infrastructure/Authentication/PasswordHasherService.cs", lang="cs", code=F["hasher"]), dict(name="BankingApp.Infrastructure/Persistence/Configurations/CustomerConfiguration.cs", lang="cs", code=F["cfg_customer2"]), dict(name="BankingApp.Infrastructure/Persistence/Configurations/AccountConfiguration.cs", lang="cs", code=F["cfg_account"]), dict(name="BankingApp.Infrastructure/Persistence/BankingAppContext.cs", lang="cs", code=F["ctx2"]), dict(name="BankingApp.Infrastructure/Repositories/CustomerRepository.cs", lang="cs", code=F["repo2"]), dict(name="BankingApp.Infrastructure/DependencyInjection.cs", lang="cs", code=F["infra_di2"]), dict(name="Terminal (migrations)", lang="sh", code=F["mig2"])],
      check="Applying migration '20261104100000_AddCredentialsAndAccounts'.\nDone."),
 dict(t="Api: métodos anónimos e método autenticado", intro="Register e Login têm [AllowAnonymous]. O RetrieveDashboard está num controller com [Authorize]: sem token válido, a API continua a responder 200, mas com success false e o erro unauthorized (é para isso que serve o RpcJwtBearerEvents). O id do cliente vem do token.",
      steps=["Criar os DTOs de Register, Login e Dashboard", "Criar o AuthController com Register e Login anónimos", "Criar o DashboardController com RetrieveDashboard autenticado", "Criar o RpcJwtBearerEvents e atualizar o Program.cs", "Apagar o CustomersController"],
      files=[dict(name="BankingApp.Api/Contracts/Auth/RegisterRequest.cs", lang="cs", code=F["contracts2"]), dict(name="BankingApp.Api/Contracts/Auth/RegisterResponse.cs", lang="cs", code=F["reg_resp"]), dict(name="BankingApp.Api/Contracts/Auth/LoginRequest.cs", lang="cs", code=F["login_req"]), dict(name="BankingApp.Api/Contracts/Auth/LoginResponse.cs", lang="cs", code=F["login_resp"]), dict(name="BankingApp.Api/Contracts/Dashboard/DashboardAccountResponse.cs", lang="cs", code=F["dash_acc_resp"]), dict(name="BankingApp.Api/Contracts/Dashboard/DashboardResponse.cs", lang="cs", code=F["dash_resp"]), dict(name="BankingApp.Api/Controllers/AuthController.cs", lang="cs", code=F["ctrl_auth"]), dict(name="BankingApp.Api/Controllers/DashboardController.cs", lang="cs", code=F["ctrl_dash"]), dict(name="BankingApp.Api/Authentication/RpcJwtBearerEvents.cs", lang="cs", code=F["rpc_events"]), dict(name="BankingApp.Api/Program.cs", lang="cs", code=F["program2"])]),
 dict(t="Bruno: configurar o Authorize passo a passo", intro="O Bruno é uma alternativa ao Postman: guarda a coleção em ficheiros de texto (.bru), que podes pôr no repositório, em docs/bruno. O fluxo é fazer Login, guardar o token numa variável e usá-lo como Bearer Token.",
      bruno=[
        dict(t="Instalar e criar a coleção", d="Instala o Bruno (usebruno.com). Em Collections escolhe Create Collection, dá-lhe o nome BankingApp e guarda-a numa pasta do repositório, por exemplo docs/bruno."),
        dict(t="Criar o ambiente Local", d="No canto superior direito, abre o seletor de ambientes e escolhe Configure. Cria o ambiente Local com a variável baseUrl, com o endereço https com que a Api arranca (está no launchSettings.json). Depois seleciona o ambiente Local."),
        dict(t="Pedido Register (anónimo)", d="New Request, método POST, URL {{baseUrl}}/api/auth/register. No separador Body escolhe JSON e escreve o corpo. O separador Auth fica em No Auth. Envia: esperas HTTP 200 com success true."),
        dict(t="Pedido Login e guardar o token", d="Novo pedido POST {{baseUrl}}/api/auth/login com email e password. No separador Vars, secção Post Response, acrescenta a variável token com o valor res.body.data.accessToken (o token vem dentro de data). Cada vez que fizeres Login, o token novo fica guardado."),
        dict(t="Pedido RetrieveDashboard (autenticado)", d="Novo pedido POST {{baseUrl}}/api/dashboard/retrieve, com o corpo JSON {}. No separador Auth escolhe Bearer Token e escreve {{token}} no campo Token. O Bruno envia o cabeçalho Authorization: Bearer <token>."),
        dict(t="Experimentar os dois resultados", d="Corre o Login e depois o RetrieveDashboard: esperas success true com as contas em data. Muda o Auth do RetrieveDashboard para No Auth e envia outra vez: continua a ser HTTP 200, mas com success false e o erro unauthorized. Isso prova que o [Authorize] está a funcionar."),
        dict(t="Se der erro de certificado", d="Em desenvolvimento, o certificado HTTPS é local. Na primeira execução o IDE pergunta se queres confiar nele: aceita. Se o Bruno continuar a recusar, desativa a verificação do certificado SSL nas preferências (só em desenvolvimento)."),
        dict(t="Opcional: autenticação ao nível da coleção", d="Nas definições da coleção, separador Auth, escolhe Bearer Token com {{token}}. Nos pedidos que precisam de token, põe o modo Inherit. Evita repetir a configuração em cada pedido."),
      ],
      files=[dict(name="docs/bruno/BankingApp/bruno.json", lang="bru", code=F["bru_json"]), dict(name="docs/bruno/BankingApp/environments/Local.bru", lang="bru", code=F["bru_env"]), dict(name="docs/bruno/BankingApp/Register.bru", lang="bru", code=F["bru_register"]), dict(name="docs/bruno/BankingApp/Login.bru", lang="bru", code=F["bru_login"]), dict(name="docs/bruno/BankingApp/RetrieveDashboard.bru", lang="bru", code=F["bru_dash"])]),
 dict(t="Testes aos handlers de autenticação", intro="Os handlers dependem de interfaces, por isso testam-se com mocks: sem base de dados e sem gerar tokens reais.",
      files=[dict(name="BankingApp.Tests/Application/LoginHandlerTests.cs", lang="cs", code=F["tests2"])],
      check="Test Explorer\n9 passed, 0 failed, 0 skipped"),
 dict(t="Verificar", intro="Confirma os cinco casos antes de avançares.",
      steps=["POST /api/auth/register válido: success true com o número da primeira conta", "Repetir o Register com o mesmo email e NIF: success false com dois erros conflict", "POST /api/auth/login com password errada: success false, erro unauthorized", "POST /api/dashboard/retrieve sem token: success false, erro unauthorized (e HTTP 200)", "POST /api/dashboard/retrieve com o token do Login: success true com uma conta e saldo 0"],
      check="register         -> success: true\nregister repetido -> success: false  [conflict, conflict]\nlogin errado     -> success: false  [unauthorized]\ndashboard s/ token -> success: false [unauthorized]\ndashboard c/ token -> success: true\n(todos com HTTP 200)"),
]

FEATURES = [
 dict(id="F1", t="Abrir conta adicional", story="Como cliente autenticado, quero abrir uma conta nova para separar o meu dinheiro.",
      endpoint="POST /api/accounts/open", body='{ "initialDeposit": 100.00 }',
      rules=["O número da conta é gerado pelo sistema e é único", "O depósito inicial não pode ser negativo", "Um cliente tem no máximo 5 contas ativas", "O cliente vem do token, nunca do corpo do pedido"],
      responses=[["success", "Conta criada, com o número da conta nova em data"], ["validation", "Depósito inicial negativo"], ["unauthorized", "Sem token válido"], ["conflict", "Já tem 5 contas ativas"]],
      criteria=["A regra das 5 contas está no Domain ou no handler, e sei explicar porquê", "A resposta traz o número da conta criada", "Há testes ao limite (4, 5 e 6 contas)", "O pedido está na coleção do Bruno"],
      uses=["dotnet-6", "csharp-2"], hint=dict(more="Pensa onde vive a regra «máximo de 5 contas». Se está no Customer (por exemplo, um método OpenAccount), o Domain protege-se a si próprio. Se está no handler, tens de repetir a verificação em todos os sítios que abram contas.", tryit="Escreve primeiro o teste que falha com a sexta conta e só depois a implementação.")),
 dict(id="F2", t="Consultar contas", story="Como cliente, quero ver as minhas contas e o detalhe de cada uma.",
      endpoint="POST /api/accounts/list  ·  POST /api/accounts/get", body='{ "status": "Active" }',
      rules=["Só devolve contas do cliente autenticado", "Uma conta de outro cliente responde not_found, igual a uma conta inexistente", "Filtro opcional status (Active ou Closed), enviado no corpo", "O detalhe (get) recebe o número da conta no corpo: { \"number\": \"AC-123456\" }", "Ordenado por número"],
      responses=[["success", "Lista ou detalhe da conta"], ["unauthorized", "Sem token válido"], ["not_found", "A conta não existe ou não é do cliente"]],
      criteria=["Não é possível ver contas de outro cliente (testado)", "O filtro por estado é feito na base de dados, não em memória", "Usa AsNoTracking nas consultas", "Os pedidos estão na coleção do Bruno"],
      uses=["dotnet-4", "csharp-3"], hint=dict(more="Responder not_found em vez de forbidden para contas de outros clientes evita revelar que o número existe. O filtro construído com IQueryable só vai à base de dados no fim, por isso podes acrescentar o Where apenas quando o parâmetro vier preenchido.", pit="Chamar ToList antes do Where traz todas as contas de todos os clientes para memória.")),
 dict(id="F3", t="Fechar conta", story="Como cliente, quero fechar uma conta que já não uso.",
      endpoint="POST /api/accounts/close", body='{ "number": "AC-123456" }',
      rules=["Só se o saldo for zero", "Uma conta já fechada não pode voltar a ser fechada", "Fechar não apaga: o estado passa a Closed", "Não pode fechar a última conta ativa"],
      responses=[["success", "Conta fechada"], ["unauthorized", "Sem token válido"], ["not_found", "A conta não existe ou não é do cliente"], ["conflict", "Saldo diferente de zero, já fechada ou última conta ativa"]],
      criteria=["A mudança de estado é um método da entidade Account", "Cada uma das três regras tem um teste", "O dashboard deixa de mostrar a conta fechada", "O pedido está na coleção do Bruno"],
      uses=["csharp-2", "dotnet-6"], hint=dict(more="O estado só deve mudar por um método da própria Account (por exemplo, Close), que valida as regras. Assim, nenhum handler consegue fechar uma conta com saldo.")),
 dict(id="F4", t="Depósito", story="Como cliente, quero depositar dinheiro numa das minhas contas.",
      endpoint="POST /api/accounts/deposit", body='{ "number": "AC-123456", "amount": 250.00, "description": "Salary" }',
      rules=["Nova entidade Transaction: tipo, valor, saldo depois do movimento, descrição e data (UTC)", "O valor tem de ser maior que zero e ter no máximo duas casas decimais", "A conta tem de estar ativa", "O saldo e a Transaction são gravados juntos, numa só chamada a SaveChanges"],
      responses=[["success", "Movimento criado, com o novo saldo"], ["validation", "Valor inválido"], ["unauthorized", "Sem token válido"], ["not_found", "A conta não existe ou não é do cliente"], ["conflict", "Conta fechada"]],
      criteria=["A entidade Transaction tem configuração e migration", "Account.Deposit atualiza o saldo e o handler cria a Transaction", "Há Theory para os valores inválidos (0, negativo, três casas)", "O pedido está na coleção do Bruno"],
      uses=["dotnet-4", "dotnet-5"], hint=dict(more="Pensa em quem cria a Transaction: o método Deposit da conta pode devolvê-la, para garantir que o saldo e o movimento nunca ficam desalinhados. O campo BalanceAfter permite reconstruir o extrato sem recalcular tudo.", pit="Fazer duas gravações separadas (saldo e movimento). Se a segunda falhar, ficas com dinheiro sem movimento.")),
 dict(id="F5", t="Levantamento", story="Como cliente, quero levantar dinheiro de uma das minhas contas.",
      endpoint="POST /api/accounts/withdraw", body='{ "number": "AC-123456", "amount": 80.00, "description": "ATM" }',
      rules=["As regras de valor e de conta ativa do depósito aplicam-se aqui", "Não pode ficar com saldo negativo: erro conflict próprio («Insufficient funds»)", "Limite diário de 500 € por conta, somando os levantamentos do dia (UTC)", "A soma do dia é calculada na base de dados"],
      responses=[["success", "Movimento criado, com o novo saldo"], ["validation", "Valor inválido"], ["unauthorized", "Sem token válido"], ["not_found", "A conta não existe ou não é do cliente"], ["conflict", "Saldo insuficiente, limite diário ou conta fechada"]],
      criteria=["O saldo insuficiente é devolvido como Response.Fail, sem lançar exceção", "O limite diário usa SumAsync na base de dados", "Há testes ao limite exato (500 permitido, 500,01 recusado)", "O pedido está na coleção do Bruno"],
      uses=["csharp-3", "dotnet-4"], hint=dict(more="Para o limite diário precisas de uma consulta ao repositório (por exemplo, a soma dos levantamentos de hoje). Define esse método no contrato da Application e implementa-o na Infrastructure com Where e SumAsync.", tryit="Faz dois levantamentos de 300 € seguidos e confirma que o segundo é recusado.")),
 dict(id="F7", t="Transferência entre contas", story="Como cliente, quero transferir dinheiro de uma das minhas contas para outra conta do banco.",
      endpoint="POST /api/transfers/create", body='{ "fromAccount": "AC-123456", "toAccount": "AC-654321", "amount": 50.00, "description": "Rent" }',
      rules=["A origem tem de ser do cliente autenticado; o destino pode ser de qualquer cliente", "Origem e destino têm de ser diferentes e ambos ativos", "As regras de saldo e de limite diário da origem aplicam-se", "Cria duas Transaction (saída e entrada) e grava tudo numa só chamada a SaveChanges", "Se algo falhar, nada é gravado"],
      responses=[["success", "Transferência feita, com o novo saldo da origem"], ["validation", "Valor inválido ou contas iguais"], ["unauthorized", "Sem token válido"], ["not_found", "Origem não é do cliente ou destino não existe"], ["conflict", "Saldo insuficiente, limite diário ou conta fechada"]],
      criteria=["Os dois movimentos e os dois saldos mudam na mesma gravação", "Há um teste que prova que, se a regra falha, nenhum saldo muda", "O destino inexistente devolve o erro not_found", "O pedido está na coleção do Bruno"],
      uses=["dotnet-4", "dotnet-6"], hint=dict(more="O SaveChangesAsync grava tudo o que o DbContext está a acompanhar numa única transação. Se carregares as duas contas e alterares os dois saldos antes de gravar, ou grava tudo ou não grava nada. Reutiliza os métodos de depósito e levantamento das entidades.", pit="Gravar a origem e depois o destino em chamadas separadas. Se a segunda falhar, o dinheiro desaparece.")),
 dict(id="F9", t="Extrato com filtros e paginação", story="Como cliente, quero consultar os movimentos de uma conta, filtrando por tipo e datas.",
      endpoint="POST /api/accounts/list-transactions", body='{ "number": "AC-123456", "type": "Deposit", "from": "2026-01-01", "to": "2026-01-31", "page": 1, "pageSize": 20 }',
      rules=["Ordenado do mais recente para o mais antigo", "Filtros opcionais: tipo, data inicial e data final", "Paginação: página 1 por omissão, 20 por página por omissão, máximo 100", "A resposta inclui os itens, o total, a página e o tamanho da página", "Consulta só de leitura, com o filtro e a paginação feitos na base de dados"],
      responses=[["success", "Página de movimentos"], ["validation", "pageSize acima de 100 ou datas trocadas"], ["unauthorized", "Sem token válido"], ["not_found", "A conta não existe ou não é do cliente"]],
      criteria=["Usa IQueryable: Where condicional, OrderByDescending, Skip e Take", "O total vem de uma consulta Count, não de carregar tudo", "Usa AsNoTracking", "O pedido está na coleção do Bruno"],
      uses=["csharp-3", "dotnet-4"], hint=dict(more="Constrói a consulta por partes: começa com os movimentos da conta, acrescenta cada Where só se o filtro vier preenchido, faz o Count, e só no fim aplica o Skip e o Take. Nada corre na base de dados até ao ToListAsync e ao CountAsync.", pit="Aplicar a paginação em memória, depois de ToList.")),
 dict(id="F10", t="Dashboard completo", story="Como cliente, quero ver no dashboard o que se passou no último mês.",
      endpoint="POST /api/dashboard/retrieve", body=None,
      rules=["Acrescenta os últimos 5 movimentos de todas as contas, do mais recente para o mais antigo", "Acrescenta o total depositado e o total levantado no mês corrente", "As transferências contam como depósito e levantamento", "O número de consultas à base de dados é fixo e não cresce com o número de contas"],
      responses=[["success", "Dashboard completo"], ["unauthorized", "Sem token válido"]],
      criteria=["Não há consulta dentro de um ciclo (sem N+1)", "Os totais são calculados na base de dados", "A resposta antiga continua válida (campos novos, nenhum removido)", "O pedido está na coleção do Bruno"],
      uses=["csharp-3", "dotnet-4"], hint=dict(more="Pede ao repositório os movimentos já filtrados (clientes, mês) e agrega com GroupBy e Sum. Se tiveres de fazer uma consulta por conta, estás a cair no N+1.")),
 dict(id="T1", kind="T", t="Testes", story="Quero ter confiança para alterar o código sem medo.",
      endpoint=None, body=None,
      rules=["Pelo menos um teste por handler, incluindo o caso de erro", "Pelo menos um Theory com valores-limite", "As regras do Domain têm testes sem mocks", "Os testes passam todos em menos de 10 segundos"],
      responses=[], criteria=["Todos os handlers têm testes", "Nenhum teste usa base de dados real", "Os nomes seguem Method_Scenario_Result", "Consigo mostrar a cobertura e explicar o que ficou por testar"],
      uses=["dotnet-5"], hint=dict(more="Começa pelos handlers com mais regras (levantamento e transferência). Um mock do repositório devolve a conta que quiseres, e o Received/DidNotReceive confirma se houve gravação.")),
 dict(id="T2", kind="T", t="Logging e middleware de tempos", story="Quero perceber o que a API está a fazer quando algo corre mal.",
      endpoint=None, body=None,
      rules=["Cada operação de escrita regista uma mensagem ILogger com marcadores (por exemplo {AccountNumber} e {Amount})", "Um middleware próprio mede a duração de cada pedido e regista um aviso se passar de 500 ms", "Nunca se regista a password nem o token"],
      responses=[], criteria=["As mensagens usam marcadores nomeados, não concatenação", "O middleware está registado na ordem certa", "Nenhum log contém dados sensíveis"],
      uses=["dotnet-2", "dotnet-3"], hint=dict(more="O middleware segue o padrão do ExceptionMiddleware (que já responde sempre 200): código antes de _next(context) corre à ida, o que está depois corre à volta, e aí já podes ler o tempo que passou (Stopwatch).")),
 dict(id="T3", kind="T", t="Coleção do Bruno e README", story="Quero que um colega consiga correr e experimentar a API em cinco minutos.",
      endpoint=None, body=None,
      rules=["A coleção em docs/bruno tem um pedido por endpoint, com o token guardado no Login", "O README explica como criar a base de dados, definir o segredo do JWT e correr a API"],
      responses=[], criteria=["Um colega consegue seguir o README sem te perguntar nada", "Todos os pedidos da coleção funcionam por ordem"],
      uses=["academia-software"], hint=dict(more="Escreve o README como se fosses tu a chegar ao projeto pela primeira vez: pré-requisitos, comandos pela ordem certa, e o que deves ver no ecrã a cada passo.")),
]

