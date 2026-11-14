namespace BankingApp.Application.Abstractions;

public class TokenResult
{
    public string AccessToken { get; init; } = "";
    public DateTime ExpiresAtUtc { get; init; }
}
