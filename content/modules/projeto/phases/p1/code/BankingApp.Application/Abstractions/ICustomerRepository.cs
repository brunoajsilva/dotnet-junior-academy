using BankingApp.Domain.Customers;

namespace BankingApp.Application.Abstractions;

public interface ICustomerRepository
{
    Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct);
    Task<IReadOnlyList<Customer>> ListAsync(CancellationToken ct);
    Task AddAsync(Customer customer, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}
