using BankingApp.Application.Handlers.CommandHandlers.Register;


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
}
