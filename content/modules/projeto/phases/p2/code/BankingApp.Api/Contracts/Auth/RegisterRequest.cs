using System.ComponentModel.DataAnnotations;

namespace BankingApp.Api.Contracts.Auth;

public class RegisterRequest
{
    [Required, StringLength(100)]
    public string Name { get; set; } = "";

    [Required, RegularExpression(@"^\d{9}$")]
    public string TaxId { get; set; } = "";

    [Required, EmailAddress]
    public string Email { get; set; } = "";

    [Required, MinLength(8)]
    public string Password { get; set; } = "";
}
