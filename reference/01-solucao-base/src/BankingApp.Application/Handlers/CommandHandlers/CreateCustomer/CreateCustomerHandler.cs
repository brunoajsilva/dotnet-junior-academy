using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Domain.Customers;

namespace BankingApp.Application.Handlers.CommandHandlers.CreateCustomer;

// handler: the use case. Business errors come back in the Response, they are not thrown
public class CreateCustomerHandler : IHandler<CreateCustomerCommand, CustomerResult>
{
    private readonly ICustomerRepository _customers;

    public CreateCustomerHandler(ICustomerRepository customers) => _customers = customers;

    public async Task<Response<CustomerResult>> HandleAsync(CreateCustomerCommand request, CancellationToken ct)
    {
        if (await _customers.ExistsByTaxIdAsync(request.TaxId, ct))
            return Response<CustomerResult>.Fail(
                Error.Conflict($"A customer with tax id {request.TaxId} already exists."));

        var customer = new Customer(request.Name, request.TaxId);

        await _customers.AddAsync(customer, ct);
        await _customers.SaveChangesAsync(ct);

        return Response<CustomerResult>.Ok(CustomerResult.From(customer));
    }
}
