// no value
static async Task SaveAsync(Account a)
{
    await Task.Delay(100);
}

// with a value
static async Task<decimal> GetBalanceAsync(string code)
{
    await Task.Delay(200);   // simulates an external call
    return 1.04m;
}

decimal c = await GetBalanceAsync("AC-001");
Task<decimal> t = GetBalanceAsync("AC-002");  // only starts
decimal d = await t;                        // waits here
