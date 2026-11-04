using var cts = new CancellationTokenSource(1000);   // 1 s
// cts.Cancel();   // or cancel manually

try { await GetBalanceAsync("AC-001", cts.Token); }
catch (OperationCanceledException)
{ Console.WriteLine("Cancelled"); }

static async Task<decimal> GetBalanceAsync(
    string code, CancellationToken ct)
{
    await Task.Delay(200, ct);   // throws if cancelled
    ct.ThrowIfCancellationRequested();
    return 1.04m;
}
