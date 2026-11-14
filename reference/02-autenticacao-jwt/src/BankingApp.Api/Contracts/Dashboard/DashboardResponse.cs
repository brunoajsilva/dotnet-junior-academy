using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;


namespace BankingApp.Api.Contracts.Dashboard;

public class DashboardResponse
{
    public string CustomerName { get; init; } = "";
    public string Email { get; init; } = "";
    public decimal TotalBalance { get; init; }
    public IReadOnlyList<DashboardAccountResponse> Accounts { get; init; } = [];

    public static DashboardResponse From(DashboardResult result) => new()
    {
        CustomerName = result.CustomerName,
        Email = result.Email,
        TotalBalance = result.TotalBalance,
        Accounts = result.Accounts.Select(DashboardAccountResponse.From).ToList()
    };
}
