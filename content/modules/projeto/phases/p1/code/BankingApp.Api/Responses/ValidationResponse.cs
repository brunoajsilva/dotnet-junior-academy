using BankingApp.Application.Common;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Responses;

public static class ValidationResponse
{
    // [ApiController] would answer 400 + ProblemDetails when the DTO is invalid.
    // In an RPC API, we answer 200 and put every invalid field in the errors list.
    public static IActionResult Create(ActionContext context)
    {
        var errors = context.ModelState
            .Where(entry => entry.Value is { Errors.Count: > 0 })
            .SelectMany(entry => entry.Value!.Errors
                .Select(e => Error.Validation($"{entry.Key}: {e.ErrorMessage}")))
            .ToList();

        return new OkObjectResult(Response<object>.Fail(errors));
    }
}
