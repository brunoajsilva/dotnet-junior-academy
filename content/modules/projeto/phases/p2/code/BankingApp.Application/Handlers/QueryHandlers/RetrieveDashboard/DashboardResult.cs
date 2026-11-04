
namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class DashboardResult
{
    public string CustomerName { get; init; } = "";
    public string Email { get; init; } = "";
    public decimal TotalBalance { get; init; }
    public IReadOnlyList<DashboardAccount> Accounts { get; init; } = [];
}
