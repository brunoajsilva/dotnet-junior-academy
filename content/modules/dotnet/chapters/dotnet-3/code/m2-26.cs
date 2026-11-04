public class AccountService
{
    readonly StandardInterest _calc = new();

    public decimal Interest(Account a)
        => _calc.Calculate(a);
}
