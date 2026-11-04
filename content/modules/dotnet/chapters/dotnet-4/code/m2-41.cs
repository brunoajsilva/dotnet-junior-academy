var highBalance = await _ctx.Accounts
    .Where(a => a.Balance > 300m)
    .OrderBy(a => a.Number)
    .ToListAsync();

var account = await _ctx.Accounts
    .Include(a => a.Customer)
    .FirstOrDefaultAsync(a => a.Number == number);

var total = await _ctx.Accounts
    .Where(a => a.CustomerId == id)
    .SumAsync(a => a.Balance);
