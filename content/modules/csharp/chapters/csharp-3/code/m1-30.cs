ICollection<Account> col = new List<Account>();

col.Add(added);                  // adds
col.Remove(old);             // removes
Console.WriteLine(col.Count);   // how many
bool exists = col.Contains(added);
col.Clear();                    // empties

// query the collection with LINQ
var highBalance = col.Where(a => a.Balance > 300m).ToList();
