using BankingApp.Application.Abstractions;
using Microsoft.AspNetCore.Identity;

namespace BankingApp.Infrastructure.Authentication;

// uses the hasher from ASP.NET Core Identity (salted, slow on purpose), without the rest of Identity
public class PasswordHasherService : IPasswordHasher
{
    private readonly PasswordHasher<object> _hasher = new();

    public string Hash(string password)
        => _hasher.HashPassword(null!, password);

    public bool Verify(string hash, string password)
        => _hasher.VerifyHashedPassword(null!, hash, password) != PasswordVerificationResult.Failed;
}
