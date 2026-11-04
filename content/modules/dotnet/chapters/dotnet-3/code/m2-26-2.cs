public class AccountService
{
    readonly IInterestCalculator _calc;

    public AccountService(
        IInterestCalculator calc)
        => _calc = calc;
}
