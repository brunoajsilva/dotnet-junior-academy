using BankingApp.Application.Abstractions;
using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;
using BankingApp.Application.Handlers.QueryHandlers.ListCustomers;
using Microsoft.Extensions.DependencyInjection;

namespace BankingApp.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IHandler<CreateCustomerCommand, CustomerResult>, CreateCustomerHandler>();
        services.AddScoped<IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>>, ListCustomersHandler>();
        return services;
    }
}
