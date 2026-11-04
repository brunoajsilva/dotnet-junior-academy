using BankingApp.Application.Common;
using BankingApp.Domain.Common;

namespace BankingApp.Api.Middleware;

public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionMiddleware> _logger;

    public ExceptionMiddleware(RequestDelegate next, ILogger<ExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            Error error;

            if (ex is DomainException)
            {
                error = Error.Validation(ex.Message);   // a rule of the Domain refused the data
            }
            else
            {
                _logger.LogError(ex, "Unhandled error on {Path}", context.Request.Path);
                error = Error.Unexpected();              // never leak the details to the client
            }

            // RPC: the call reached the server, so the HTTP answer is always 200
            context.Response.StatusCode = StatusCodes.Status200OK;
            await context.Response.WriteAsJsonAsync(Response<object>.Fail(error));
        }
    }
}

// An exception is for the unexpected. Expected errors (not found, conflict)
// are returned by the handlers, as Response.Fail(...).
