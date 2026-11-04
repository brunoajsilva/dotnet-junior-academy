protected override void OnModelCreating(ModelBuilder mb)
{
    mb.Entity<Account>(e =>
    {
        e.Property(a => a.Number).HasMaxLength(20);
        e.HasIndex(a => a.Number).IsUnique();
        e.Property(a => a.Balance).HasPrecision(18, 2);
        e.HasOne(a => a.Customer)
            .WithMany(c => c.Accounts)
            .HasForeignKey(a => a.CustomerId);
    });
}
