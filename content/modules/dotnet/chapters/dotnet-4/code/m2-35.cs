public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public List<Account> Accounts { get; } = new();
}

public class Account
{
    public int Id { get; set; }
    public string Number { get; set; } = "";
    public decimal Balance { get; set; }
    public int CustomerId { get; set; }
    public Customer Customer { get; set; } = null!;
}
