using System.ComponentModel.DataAnnotations;

namespace BankingApp.Api.Contracts.Customers;

public class NewCustomer
{
    [Required, StringLength(100)]
    public string Name { get; set; } = "";

    [Required, RegularExpression(@"^\d{9}$")]
    public string TaxId { get; set; } = "";
}
