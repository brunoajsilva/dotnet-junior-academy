public interface IInterestCalculator
{
    decimal Calculate(Account account);
}

public class StandardInterest : IInterestCalculator
{
    public decimal Calculate(Account a) => a.Balance * 0.01m;
}

public class PromoInterest : IInterestCalculator
{
    private readonly decimal _rate;
    public PromoInterest(decimal rate) => _rate = rate;
    public decimal Calculate(Account a)
        => a.Balance * _rate;
}
