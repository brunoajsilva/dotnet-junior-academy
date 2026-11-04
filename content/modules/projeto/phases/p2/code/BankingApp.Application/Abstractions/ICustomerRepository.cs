using BankingApp.Domain.Customers;

namespace BankingApp.Application.Abstractions;

public interface ICustomerRepository
{
    Task<bool> ExistsByEmailAsync(string email, CancellationToken ct);
    Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct);
    Task<Customer?> GetByEmailAsync(string email, CancellationToken ct);
    Task<Customer?> GetByIdWithAccountsAsync(int id, CancellationToken ct);
    Task AddAsync(Customer customer, CancellationToken ct);
    Task SaveChangesAsync(CancellationToken ct);
}
