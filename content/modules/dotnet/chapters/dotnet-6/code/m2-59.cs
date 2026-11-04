public record OpenAccountCommand(
    string Number, int CustomerId, decimal Balance);

public class OpenAccountHandler
{
    private readonly IAccountRepository _repo;
    public OpenAccountHandler(IAccountRepository repo)
        => _repo = repo;

    public async Task<string> Handle(OpenAccountCommand c)
    {
        var acc = new Account(
            c.Number, c.CustomerId, c.Balance);
        await _repo.AddAsync(acc);
        return acc.Number;
    }
}
