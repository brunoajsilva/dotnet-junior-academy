namespace BankingApp.Application.Common;

// the output of EVERY use case: success is just "no errors"
public class Response<T>
{
    public bool Success => Errors.Count == 0;
    public T? Data { get; init; }
    public IReadOnlyList<Error> Errors { get; init; } = [];

    public static Response<T> Ok(T data) => new() { Data = data };

    public static Response<T> Fail(params IEnumerable<Error> errors)
        => new() { Errors = errors.ToList() };

    // convert the data (for example, a result into a DTO) and keep the errors
    public Response<TOut> Map<TOut>(Func<T, TOut> map)
        => Success ? Response<TOut>.Ok(map(Data!)) : Response<TOut>.Fail(Errors);
}
