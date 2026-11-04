public class Result<T>
{
    public bool Success { get; }
    public T? Value { get; }
    public string? Error { get; }

    public Result(T value)
        => (Success, Value) = (true, value);
    public Result(string error) => Error = error;
}

static T Max<T>(T a, T b) where T : IComparable<T>
    => a.CompareTo(b) >= 0 ? a : b;

var r = new Result<decimal>(320.5m);
var m = Max(3, 7);          // T is int
var p = Max("Ana", "Rui");  // T is string
