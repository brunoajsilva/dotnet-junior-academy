using BankingApp.Domain.Common;
using BankingApp.Domain.Customers;

namespace BankingApp.Domain.Accounts;

public class Account
{
    private Account() { }   // required by EF Core

    public static Account Open(string number, Customer customer, decimal initialDeposit, DateOnly opened)
    {
        if (string.IsNullOrWhiteSpace(number))
            throw new DomainException("Number is required.");
        if (initialDeposit < 0)
            throw new DomainException("Initial deposit cannot be negative.");

        return new Account
        {
            Number = number,
            Customer = customer,
            Balance = initialDeposit,
            Opened = opened,
            Status = AccountStatus.Active
        };
    }

    public int Id { get; private set; }
    public string Number { get; private set; } = "";
    public int CustomerId { get; private set; }
    public Customer Customer { get; private set; } = null!;
    public decimal Balance { get; private set; }
    public DateOnly Opened { get; private set; }
    public AccountStatus Status { get; private set; }
}
