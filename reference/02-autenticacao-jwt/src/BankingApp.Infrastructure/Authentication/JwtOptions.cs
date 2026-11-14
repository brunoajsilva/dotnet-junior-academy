namespace BankingApp.Infrastructure.Authentication;

public class JwtOptions
{
    public string Issuer { get; set; } = "";
    public string Audience { get; set; } = "";
    public string Key { get; set; } = "";          // comes from appsettings.json
    public int ExpiresMinutes { get; set; } = 60;
}
