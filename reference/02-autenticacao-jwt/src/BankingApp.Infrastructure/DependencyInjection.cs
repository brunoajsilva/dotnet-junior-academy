using BankingApp.Application.Abstractions;
using BankingApp.Infrastructure.Authentication;
using BankingApp.Infrastructure.Persistence;
using BankingApp.Infrastructure.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<BankingAppContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("BankingApp")));

        services.Configure<JwtOptions>(configuration.GetSection("Jwt"));

        services.AddScoped<ICustomerRepository, CustomerRepository>();
        services.AddSingleton<IPasswordHasher, PasswordHasherService>();
        services.AddScoped<ITokenService, JwtTokenService>();
        return services;
    }
}
