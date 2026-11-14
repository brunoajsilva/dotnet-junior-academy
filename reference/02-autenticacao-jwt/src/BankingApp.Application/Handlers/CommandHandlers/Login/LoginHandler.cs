using BankingApp.Application.Abstractions;
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
}
