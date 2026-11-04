// packages (Api project)
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design

// CLI tool (once per machine)
dotnet tool install --global dotnet-ef

// appsettings.json
"ConnectionStrings": {
  "BankingApp": "Server=...;Database=BankingApp"
}
