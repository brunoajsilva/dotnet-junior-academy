public class BankingAppContext : DbContext
{
    public BankingAppContext(
        DbContextOptions<BankingAppContext> options)
        : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Account> Accounts => Set<Account>();
}

// Program.cs
builder.Services.AddDbContext<BankingAppContext>(o =>
    o.UseSqlServer(cs));
