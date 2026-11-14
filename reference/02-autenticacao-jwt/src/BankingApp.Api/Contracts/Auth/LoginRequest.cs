using System.ComponentModel.DataAnnotations;

namespace BankingApp.Api.Contracts.Auth;

public class LoginRequest
{
    [Required, EmailAddress]
    public string Email { get; set; } = "";

    [Required]
    public string Password { get; set; } = "";
}
