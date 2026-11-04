public class Customer
{
    public string Name { get; }
    public string TaxId { get; }

    public Customer(string name, string nif)
    {
        Name = name;
        TaxId = nif;
    }
}

public record Account(
    string Number,
    Customer AccountHolder,
    decimal Balance);
