using BankingApp.Api.Contracts.Auth;
using BankingApp.Application.Abstractions;
using BankingApp.Application.Common;
using BankingApp.Application.Handlers.CommandHandlers.Login;
using BankingApp.Application.Handlers.CommandHandlers.Register;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BankingApp.Api.Controllers;

[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    private readonly IHandler<RegisterCommand, RegisterResult> _register;
    private readonly IHandler<LoginCommand, LoginResult> _login;

    public AuthController(
        IHandler<RegisterCommand, RegisterResult> register,
        IHandler<LoginCommand, LoginResult> login)
    {
        _register = register;
        _login = login;
    }

    [AllowAnonymous]
    [HttpPost("register")]
    public async Task<Response<RegisterResponse>> Register(RegisterRequest body, CancellationToken ct)
    {
        var result = await _register.HandleAsync(
            new RegisterCommand { Name = body.Name, TaxId = body.TaxId, Email = body.Email, Password = body.Password }, ct);

        return result.Map(RegisterResponse.From);
    }

    [AllowAnonymous]
    [HttpPost("login")]
    public async Task<Response<LoginResponse>> Login(LoginRequest body, CancellationToken ct)
    {
        var result = await _login.HandleAsync(new LoginCommand { Email = body.Email, Password = body.Password }, ct);
        return result.Map(LoginResponse.From);
    }
}
