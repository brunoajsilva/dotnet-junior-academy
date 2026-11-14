using BankingApp.Application.Abstractions;
using BankingApp.Domain.Customers;
using BankingApp.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Repositories;

public class CustomerRepository : ICustomerRepository
{
    private readonly BankingAppContext _db;

    public CustomerRepository(BankingAppContext db) => _db = db;

    public Task<bool> ExistsByEmailAsync(string email, CancellationToken ct)
        => _db.Customers.AnyAsync(c => c.Email == email, ct);

    public Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct)
        => _db.Customers.AnyAsync(c => c.TaxId == taxId, ct);

    public Task<Customer?> GetByEmailAsync(string email, CancellationToken ct)
        => _db.Customers.FirstOrDefaultAsync(c => c.Email == email, ct);

    public Task<Customer?> GetByIdWithAccountsAsync(int id, CancellationToken ct)
        => _db.Customers.Include(c => c.Accounts)
                        .AsNoTracking()
                        .FirstOrDefaultAsync(c => c.Id == id, ct);

    public async Task AddAsync(Customer customer, CancellationToken ct)
        => await _db.Customers.AddAsync(customer, ct);

    public Task SaveChangesAsync(CancellationToken ct)
        => _db.SaveChangesAsync(ct);
}
