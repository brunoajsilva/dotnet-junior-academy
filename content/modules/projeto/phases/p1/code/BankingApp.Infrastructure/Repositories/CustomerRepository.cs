using BankingApp.Application.Abstractions;
using BankingApp.Domain.Customers;
using BankingApp.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Repositories;

public class CustomerRepository : ICustomerRepository
{
    private readonly BankingAppContext _db;

    public CustomerRepository(BankingAppContext db) => _db = db;

    public Task<bool> ExistsByTaxIdAsync(string taxId, CancellationToken ct)
        => _db.Customers.AnyAsync(c => c.TaxId == taxId, ct);

    public async Task<IReadOnlyList<Customer>> ListAsync(CancellationToken ct)
        => await _db.Customers.AsNoTracking().OrderBy(c => c.Name).ToListAsync(ct);

    public async Task AddAsync(Customer customer, CancellationToken ct)
        => await _db.Customers.AddAsync(customer, ct);

    public Task SaveChangesAsync(CancellationToken ct)
        => _db.SaveChangesAsync(ct);
}
