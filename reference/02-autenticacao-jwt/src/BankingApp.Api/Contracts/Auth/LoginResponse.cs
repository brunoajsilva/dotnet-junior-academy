using BankingApp.Application.Handlers.CommandHandlers.Login;


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
}
