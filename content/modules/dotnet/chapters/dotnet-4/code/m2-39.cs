dotnet ef migrations add Initial

Migrations/
  20261022101500_Initial.cs
  BankingAppContextModelSnapshot.cs

// 20261022101500_Initial.cs (generated)
protected override void Up(MigrationBuilder mb)
{
    mb.CreateTable(
        name: "Accounts",
        columns: table => new { ... });
}

protected override void Down(MigrationBuilder mb)
    => mb.DropTable(name: "Accounts");
