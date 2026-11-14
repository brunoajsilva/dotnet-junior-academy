using BankingApp.Domain.Accounts;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace BankingApp.Infrastructure.Persistence.Configurations;

public class AccountConfiguration : IEntityTypeConfiguration<Account>
{
    public void Configure(EntityTypeBuilder<Account> builder)
    {
        builder.Property(a => a.Number).HasMaxLength(20).IsRequired();
        builder.HasIndex(a => a.Number).IsUnique();
        builder.Property(a => a.Balance).HasPrecision(18, 2);
        builder.Property(a => a.Status).HasConversion<string>().HasMaxLength(20);

        builder.HasOne(a => a.Customer)
               .WithMany(c => c.Accounts)
               .HasForeignKey(a => a.CustomerId);
    }
}
