dotnet ef migrations add InitialCreate -p src/BankingApp.Infrastructure -s src/BankingApp.Api -o Persistence/Migrations
dotnet ef database update            -p src/BankingApp.Infrastructure -s src/BankingApp.Api
