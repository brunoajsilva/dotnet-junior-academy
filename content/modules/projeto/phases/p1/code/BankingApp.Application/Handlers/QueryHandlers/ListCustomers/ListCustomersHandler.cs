using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

namespace BankingApp.Application.Handlers.QueryHandlers.ListCustomers;

public class ListCustomersHandler : IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>>
{
    private readonly ICustomerRepository _customers;

    public ListCustomersHandler(ICustomerRepository customers) => _customers = customers;

    public async Task<Response<IReadOnlyList<CustomerResult>>> HandleAsync(ListCustomersQuery request, CancellationToken ct)
    {
        var all = await _customers.ListAsync(ct);
        return Response<IReadOnlyList<CustomerResult>>.Ok(all.Select(CustomerResult.From).ToList());
    }
}
