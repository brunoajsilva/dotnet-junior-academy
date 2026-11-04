# NuGet packages (or use the NuGet window of the IDE)
dotnet add src/BankingApp.Application    package Microsoft.Extensions.DependencyInjection.Abstractions
dotnet add src/BankingApp.Infrastructure package Microsoft.EntityFrameworkCore.SqlServer
dotnet add src/BankingApp.Api            package Microsoft.EntityFrameworkCore.Design
dotnet add src/BankingApp.Api            package Swashbuckle.AspNetCore.SwaggerUI
dotnet add tests/BankingApp.Tests        package NSubstitute

# the EF Core command-line tool, once per machine
dotnet tool install --global dotnet-ef
