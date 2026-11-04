// 1. describes the query (does not run)
IQueryable<Account> q = context.Accounts
    .Where(a => a.Balance > 300m)
    .OrderBy(a => a.Number);

// 2. generates the SQL and runs it
var lista = await q.ToListAsync();

// SELECT * FROM Accounts
// WHERE Balance > 300 ORDER BY Number
