public class DepositHandler
{
    private readonly ILogger<DepositHandler> _logger;

    public DepositHandler(ILogger<DepositHandler> logger) => _logger = logger;

    public void Handle(string accountNumber, decimal amount)
    {
        // named placeholders, not string concatenation
        _logger.LogInformation("Deposit of {Amount} into account {AccountNumber}", amount, accountNumber);
    }
}
