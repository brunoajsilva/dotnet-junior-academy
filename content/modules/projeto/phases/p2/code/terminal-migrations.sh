# if you created test customers in step 1, start clean (they have no email):
dotnet ef database drop -f -p src/BankingApp.Infrastructure -s src/BankingApp.Api

dotnet ef migrations add AddCredentialsAndAccounts -p src/BankingApp.Infrastructure -s src/BankingApp.Api -o Persistence/Migrations
dotnet ef database update                          -p src/BankingApp.Infrastructure -s src/BankingApp.Api
