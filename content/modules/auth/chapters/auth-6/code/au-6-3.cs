[Authorize]
[HttpGet("{number}")]
public IActionResult GetAccount(string number)
{
    var customerId = int.Parse(User.FindFirstValue("sub")!);
    var account = Accounts.FirstOrDefault(a => a.Number == number);

    // the account is not yours? Answer exactly as if it did not exist
    if (account is null || account.CustomerId != customerId)
        return NotFound();

    return Ok(account);
}
