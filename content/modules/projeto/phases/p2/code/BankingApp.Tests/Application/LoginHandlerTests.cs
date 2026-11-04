using BankingApp.Application.Abstractions;
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
}
