using BankingApp.Domain.Customers;

namespace BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

public class CustomerResult
{
    public int Id { get; init; }
    public string Name { get; init; } = "";
    public string TaxId { get; init; } = "";

    public static CustomerResult From(Customer customer) => new()
    {
        Id = customer.Id,
        Name = customer.Name,
        TaxId = customer.TaxId
    };
}
