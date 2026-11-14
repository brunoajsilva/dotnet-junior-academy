using BankingApp.Api.Contracts.Customers;
using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;
using BankingApp.Application.Handlers.QueryHandlers.ListCustomers;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CustomersController : ControllerBase
{
    private readonly IHandler<CreateCustomerCommand, CustomerResult> _create;
    private readonly IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>> _list;

    public CustomersController(
        IHandler<CreateCustomerCommand, CustomerResult> create,
        IHandler<ListCustomersQuery, IReadOnlyList<CustomerResult>> list)
    {
        _create = create;
        _list = list;
    }

    // RPC: every operation is a POST to /api/<area>/<action>, and the answer is always 200 OK.
    // Read "success" and "errors" in the body.
    [HttpPost("list")]
    public async Task<Response<IEnumerable<CustomerResponse>>> List(CancellationToken ct)
    {
        var result = await _list.HandleAsync(new ListCustomersQuery(), ct);
        return result.Map(items => items.Select(CustomerResponse.From));
    }

    [HttpPost("create")]
    public async Task<Response<CustomerResponse>> Create(NewCustomer body, CancellationToken ct)
    {
        var result = await _create.HandleAsync(new CreateCustomerCommand { Name = body.Name, TaxId = body.TaxId }, ct);
        return result.Map(CustomerResponse.From);
    }
}
