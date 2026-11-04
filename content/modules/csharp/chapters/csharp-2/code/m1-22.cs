public class Customer
{
    public string Name { get; set; }    // read and write
    public string TaxId { get; init; }   // only on creation
    public int Points { get; private set; } // only the class

    private string _email = "";
    public string Email
    {
        get => _email;
        set => _email = value.Trim();
    }

    public void AddPoints(int n) => Points += n;
}

var c = new Customer { Name = "Ana", TaxId = "1" };
c.Name = "Ana P.";  // c.TaxId = "2" does not compile
