using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;


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
}
