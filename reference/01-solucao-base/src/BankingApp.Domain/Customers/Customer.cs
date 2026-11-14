using BankingApp.Domain.Common;

namespace BankingApp.Domain.Customers;

public class Customer
{
    private Customer() { }   // required by EF Core

    public Customer(string name, string taxId)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Name is required.");
        if (taxId.Length != 9 || !taxId.All(char.IsDigit))
            throw new DomainException($"Invalid tax id: {taxId}");

        Name = name.Trim();
        TaxId = taxId;
    }

    public int Id { get; private set; }
    public string Name { get; private set; } = "";
    public string TaxId { get; private set; } = "";
}
