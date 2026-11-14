using BankingApp.Application.Common;
using Microsoft.AspNetCore.Authentication.JwtBearer;

namespace BankingApp.Api.Authentication;

// RPC: even "no token" and "no permission" answer 200, with the error in the body
public class RpcJwtBearerEvents : JwtBearerEvents
{
    public RpcJwtBearerEvents()
    {
        OnChallenge = context =>
        {
            context.HandleResponse();               // skip the default 401
            return Write(context.HttpContext, Error.Unauthorized("Missing or invalid token."));
        };

        OnForbidden = context =>
            Write(context.HttpContext, Error.Forbidden("You do not have permission for this operation."));
    }

    private static Task Write(HttpContext http, Error error)
    {
        http.Response.StatusCode = StatusCodes.Status200OK;
        return http.Response.WriteAsJsonAsync(Response<object>.Fail(error));
    }
}
