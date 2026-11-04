using BankingApp.Application.Abstractions;
using BankingApp.Application.Handlers.CommandHandlers.Login;
using BankingApp.Application.Handlers.CommandHandlers.Register;
using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IHandler<RegisterCommand, RegisterResult>, RegisterHandler>();
        services.AddScoped<IHandler<LoginCommand, LoginResult>, LoginHandler>();
        services.AddScoped<IHandler<RetrieveDashboardQuery, DashboardResult>, RetrieveDashboardHandler>();
        return services;
    }
}
