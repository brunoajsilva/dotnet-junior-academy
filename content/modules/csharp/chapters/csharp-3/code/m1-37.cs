// sequential: takes the sum of the times
var a = await GetBalanceAsync("AC-001");
var b = await GetBalanceAsync("AC-002");

// parallel: takes as long as the slowest
var t1 = GetBalanceAsync("AC-001");
var t2 = GetBalanceAsync("AC-002");

decimal[] prices = await Task.WhenAll(t1, t2);

// a list of codes, at most 3 at a time
await Parallel.ForEachAsync(codes,
    new ParallelOptions { MaxDegreeOfParallelism = 3 },
    async (code, ct) => await GetBalanceAsync(code));
