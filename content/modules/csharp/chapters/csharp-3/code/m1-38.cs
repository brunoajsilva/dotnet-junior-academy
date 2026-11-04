static async Task<decimal> GetBalanceAsync(string code)
{
    await Task.Delay(200);
    if (string.IsNullOrEmpty(code))
        throw new ArgumentException("Missing code");
    return 1.04m;
}

try
{
    var c = await GetBalanceAsync("");   // error is raised
}
catch (ArgumentException ex)
{ Console.WriteLine(ex.Message); }

var t = GetBalanceAsync("");   // no await: no error
