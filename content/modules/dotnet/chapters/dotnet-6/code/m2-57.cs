// Application: the contract
public interface IAccountRepository
{
    Task<Account?> GetAsync(string number);
    Task AddAsync(Account account);
}

// Infrastructure: the implementation
public class AccountRepository : IAccountRepository
{
    private readonly BankingAppContext _ctx;
    public AccountRepository(BankingAppContext c)
        => _ctx = c;

    public Task<Account?> GetAsync(string number)
        => _ctx.Accounts.FirstOrDefaultAsync(
            a => a.Number == number);
}
