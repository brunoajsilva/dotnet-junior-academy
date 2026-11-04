using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using BankingApp.Api.Contracts.Dashboard;
using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.QueryHandlers.RetrieveDashboard;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Controllers;

[ApiController]
[Route("api/dashboard")]
[Authorize]                                   // every method here requires a valid token
public class DashboardController : ControllerBase
{
    private readonly IHandler<RetrieveDashboardQuery, DashboardResult> _handler;

    public DashboardController(IHandler<RetrieveDashboardQuery, DashboardResult> handler) => _handler = handler;

    [HttpPost("retrieve")]
    public async Task<Response<DashboardResponse>> RetrieveDashboard(CancellationToken ct)
    {
        // the customer id comes from the token, never from the request
        var customerId = int.Parse(User.FindFirstValue(JwtRegisteredClaimNames.Sub)!);

        var result = await _handler.HandleAsync(new RetrieveDashboardQuery { CustomerId = customerId }, ct);
        return result.Map(DashboardResponse.From);
    }
}
