using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.Login;

public class LoginCommand : Request
{
    public string Email { get; init; } = "";
    public string Password { get; init; } = "";
}
