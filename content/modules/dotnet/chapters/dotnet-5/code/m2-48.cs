[Theory]
[InlineData(0, 200, 0)]
[InlineData(2, 200, 4)]
[InlineData(5, 200, 10)]
public void Calculate_AppliesRate(
    int ratePercent, int balance, int expected)
{
    var calc = new PromoInterest(ratePercent / 100m);
    var acc = new Account("AC-001", ana, balance);

    Assert.Equal(expected, calc.Calculate(acc));
}
