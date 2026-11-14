using BankingApp.Domain.Common;
using BankingApp.Domain.Customers;

namespace BankingApp.Tests.Domain;

public class CustomerTests
{
    [Theory]
    [InlineData("123")]
    [InlineData("12345678a")]
    [InlineData("1234567890")]
    public void Constructor_InvalidTaxId_Throws(string taxId)
        => Assert.Throws<DomainException>(() => new Customer("Ana Pereira", taxId));

    [Fact]
    public void Constructor_ValidData_TrimsTheName()
    {
        var customer = new Customer("  Ana Pereira ", "123456789");

        Assert.Equal("Ana Pereira", customer.Name);
    }
}
