
namespace BankingApp.Application.Handlers.CommandHandlers.Login;

public class LoginResult
{
    public string AccessToken { get; init; } = "";
    public DateTime ExpiresAtUtc { get; init; }
}
