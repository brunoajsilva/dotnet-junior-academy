using BankingApp.Domain.Customers;
using Microsoft.EntityFrameworkCore;

namespace BankingApp.Infrastructure.Persistence;

public class BankingAppContext : DbContext
{
    public BankingAppContext(DbContextOptions<BankingAppContext> options) : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
        => modelBuilder.ApplyConfigurationsFromAssembly(typeof(BankingAppContext).Assembly);
}
