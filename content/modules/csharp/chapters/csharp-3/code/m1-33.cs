static void Register(Account? a, string text)
{
    ArgumentNullException.ThrowIfNull(a);
    if (a.Balance < 0)
        throw new ArgumentException("Balance < 0");

    if (!decimal.TryParse(text, out var p))
        return;      // no exception
}

catch (Exception ex)
{
    Log(ex);
    throw;          // not: throw ex;
}
