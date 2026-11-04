using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.Register;

public class RegisterCommand : Request
{
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";
    public string Email { get; init; } = "";
    public string Password { get; init; } = "";
}
