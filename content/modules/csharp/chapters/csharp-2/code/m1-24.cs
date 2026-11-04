public class InterestService
{
    private readonly IInterestCalculator _calculator;

    // composition: receives the calculator from outside
    public InterestService(IInterestCalculator calculator)
        => _calculator = calculator;

    public decimal Annual(Account a)
        => _calculator.Calculate(a);
}

var normal = new InterestService(new StandardInterest());
var promo = new InterestService(new PromoInterest(0.03m));
