using BankingApp.Domain.Accounts;
using BankingApp.Domain.Common;

namespace BankingApp.Domain.Customers;

public class Customer
{
    private Customer() { }   // required by EF Core

    public Customer(string name, string taxId, string email, string passwordHash)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new DomainException("Name is required.");
        if (taxId.Length != 9 || !taxId.All(char.IsDigit))
            throw new DomainException($"Invalid tax id: {taxId}");
        if (!email.Contains('@'))
            throw new DomainException("Invalid email.");
        if (string.IsNullOrWhiteSpace(passwordHash))
            throw new DomainException("Password hash is required.");

        Name = name.Trim();
        TaxId = taxId;
        Email = email.Trim().ToLowerInvariant();
        PasswordHash = passwordHash;
    }

    public int Id { get; private set; }
    public string Name { get; private set; } = "";
    public string TaxId { get; private set; } = "";
    public string Email { get; private set; } = "";
    public string PasswordHash { get; private set; } = "";
    public List<Account> Accounts { get; private set; } = [];
}
