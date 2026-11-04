public class PromoInterestTests
{
    [Fact]
    public void Calculate_Rate2Percent_Returns2PercentOfBalance()
    {
        // Arrange
        var calc = new PromoInterest(0.02m);
        var acc = new Account("AC-001", ana, 200m);

        // Act
        var result = calc.Calculate(acc);

        // Assert
        Assert.Equal(4m, result);
    }
}
