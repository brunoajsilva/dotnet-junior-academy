public class AccountService
{
    private readonly ILogger<AccountService> _log;
    private readonly InterestOptions _options;

    public AccountService(
        ILogger<AccountService> log,
        IOptions<InterestOptions> options)
    {
        _log = log;
        _options = options.Value;
    }
}
