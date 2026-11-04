using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;

[ApiController]
[Route("api/auth")]
public class AuthController : ControllerBase
{
    // in-memory users: only for this lab (a real API stores a password HASH)
    private static readonly List<User> Users =
    [
        new(1, "ana@example.com", "Passw0rd!", "Ana Pereira", "Customer"),
        new(2, "rui@example.com", "Passw0rd!", "Rui Costa", "Manager")
    ];

    private readonly JwtSettings _jwt;

    public AuthController(JwtSettings jwt) => _jwt = jwt;

    // 1. generates the token: anonymous, because the caller does not have one yet
    [AllowAnonymous]
    [HttpPost("login")]
    public ActionResult<LoginResponse> Login(LoginRequest body)
    {
        var user = Users.FirstOrDefault(u => u.Email == body.Email && u.Password == body.Password);
        if (user is null) return Unauthorized();   // same answer for unknown email and wrong password

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim("name", user.Name),
            new Claim("role", user.Role)
        };
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwt.Key));
        var expires = DateTime.UtcNow.AddMinutes(_jwt.ExpiresMinutes);

        var token = new JwtSecurityToken(_jwt.Issuer, _jwt.Audience, claims, expires: expires,
            signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));

        return Ok(new LoginResponse(new JwtSecurityTokenHandler().WriteToken(token), expires));
    }

    // 2. authenticated: without a valid token the answer is 401
    [Authorize]
    [HttpGet("me")]
    public IActionResult Me() => Ok(new
    {
        id = User.FindFirstValue("sub"),
        name = User.FindFirstValue("name"),
        role = User.FindFirstValue("role")
    });
}

public record LoginRequest(string Email, string Password);
public record LoginResponse(string AccessToken, DateTime ExpiresAtUtc);
public record User(int Id, string Email, string Password, string Name, string Role);
