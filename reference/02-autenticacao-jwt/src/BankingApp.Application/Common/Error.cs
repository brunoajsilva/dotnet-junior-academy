namespace BankingApp.Application.Common;

// RPC: errors are data. Every use case answers with a list of Error, never with an HTTP code.
public class Error
{
    public Error(string code, string message)
    {
        Code = code;
        Message = message;
    }

    public string Code { get; }
    public string Message { get; }

    public static Error Validation(string message)   => new("validation", message);
    public static Error NotFound(string message)     => new("not_found", message);
    public static Error Conflict(string message)     => new("conflict", message);
    public static Error Unauthorized(string message) => new("unauthorized", message);
    public static Error Forbidden(string message)    => new("forbidden", message);
    public static Error Unexpected()                 => new("unexpected", "Unexpected error.");
}
