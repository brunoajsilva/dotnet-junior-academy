using BankingApp.Application.Common;

namespace BankingApp.Application.Abstractions;

// one handler per use case: a Request goes in, a Response comes out
public interface IHandler<in TRequest, TData> where TRequest : Request
{
    Task<Response<TData>> HandleAsync(TRequest request, CancellationToken ct);
}
