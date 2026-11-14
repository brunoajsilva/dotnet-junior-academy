
namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class DashboardAccount
{
    public string Number { get; init; } = "";
    public decimal Balance { get; init; }
    public string Status { get; init; } = "";
    public DateOnly Opened { get; init; }
}
