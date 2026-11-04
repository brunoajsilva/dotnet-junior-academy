var ana = new Customer("Ana Pereira", "123456789");
var accounts = new List<Account>();
accounts.Add(new Account("AC-001", ana, 320.50m));

var byNumber = new Dictionary<string, Account>();
byNumber["AC-001"] = accounts[0];

if (byNumber.TryGetValue("AC-002", out var a))
    Console.WriteLine(a.Balance);
