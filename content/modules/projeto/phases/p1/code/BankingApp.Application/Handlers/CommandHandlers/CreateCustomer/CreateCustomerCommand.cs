using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

// command: only data
public class CreateCustomerCommand : Request
{
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";
}
