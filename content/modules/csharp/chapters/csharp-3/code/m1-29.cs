var sortedAccounts = accounts
    .Where(a => a.Balance > 300m)
    .OrderByDescending(a => a.Balance)
    .Select(a => new { a.Number, a.Balance })
    .ToList();

var totals = accounts
    .GroupBy(a => a.AccountHolder.Name)
    .Select(g => new
    {
        Customer = g.Key,
        Total = g.Sum(a => a.Balance)
    });
