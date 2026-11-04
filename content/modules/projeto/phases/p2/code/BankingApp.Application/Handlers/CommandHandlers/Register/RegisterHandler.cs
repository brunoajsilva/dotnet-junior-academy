using BankingApp.Application.Abstractions;
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
}
