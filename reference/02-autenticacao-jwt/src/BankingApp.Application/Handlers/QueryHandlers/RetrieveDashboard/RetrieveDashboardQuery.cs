using BankingApp.Application.Common;

namespace BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;

public class RetrieveDashboardQuery : Request
{
    public int CustomerId { get; init; }
}
