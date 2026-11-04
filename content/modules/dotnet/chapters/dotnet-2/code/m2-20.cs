public record NewAccount(
    [Required, StringLength(20)] string Number,
    [RegularExpression(@"^\d{9}$")] string TaxId,
    [Range(0, 1000000)] decimal Balance);

public record AccountResponse(
    string Number, string Customer, decimal Balance);
