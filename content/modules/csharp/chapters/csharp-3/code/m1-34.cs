public class InvalidAccountException : Exception
{
    public string Number { get; }

    public InvalidAccountException(string num, string msg)
        : base(msg) => Number = num;
}

throw new InvalidAccountException("AC-001", "Balance < 0");

try { /* ... */ }
catch (InvalidAccountException ex)
{
    Console.WriteLine(ex.Number);
}
