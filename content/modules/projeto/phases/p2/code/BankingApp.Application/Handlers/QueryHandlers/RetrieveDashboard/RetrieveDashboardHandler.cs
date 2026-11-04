using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Domain.Accounts;

namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class RetrieveDashboardHandler : IHandler<RetrieveDashboardQuery, DashboardResult>
{
    private readonly ICustomerRepository _customers;

    public RetrieveDashboardHandler(ICustomerRepository customers) => _customers = customers;

    public async Task<Response<DashboardResult>> HandleAsync(RetrieveDashboardQuery request, CancellationToken ct)
    {
        var customer = await _customers.GetByIdWithAccountsAsync(request.CustomerId, ct);
        if (customer is null)
            return Response<DashboardResult>.Fail(Error.NotFound("Customer not found."));

        var accounts = customer.Accounts
            .Where(a => a.Status == AccountStatus.Active)
            .OrderBy(a => a.Number)
            .Select(a => new DashboardAccount
            {
                Number = a.Number,
                Balance = a.Balance,
                Status = a.Status.ToString(),
                Opened = a.Opened
            })
            .ToList();

        return Response<DashboardResult>.Ok(new DashboardResult
        {
            CustomerName = customer.Name,
            Email = customer.Email,
            TotalBalance = accounts.Sum(a => a.Balance),
            Accounts = accounts
        });
    }
}
