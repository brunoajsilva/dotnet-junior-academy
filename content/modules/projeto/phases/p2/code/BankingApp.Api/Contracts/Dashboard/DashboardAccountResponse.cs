using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;


namespace BankingApp.Api.Contracts.Dashboard;

public class DashboardAccountResponse
{
    public string Number { get; init; } = "";
    public decimal Balance { get; init; }
    public string Status { get; init; } = "";
    public DateOnly Opened { get; init; }

    public static DashboardAccountResponse From(DashboardAccount account) => new()
    {
        Number = account.Number,
        Balance = account.Balance,
        Status = account.Status,
        Opened = account.Opened
    };
}
