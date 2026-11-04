dotnet ef database update
// applies the pending migrations

// the model changes: Customer gets TaxId
dotnet ef migrations add AddTaxId
dotnet ef database update

// go back to a previous migration
dotnet ef database update Initial

// drop the last migration (not applied)
dotnet ef migrations remove

// SQL script for production
dotnet ef migrations script --idempotent
