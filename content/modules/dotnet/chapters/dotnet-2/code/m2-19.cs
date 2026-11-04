[HttpGet("{number}")]
public ActionResult<AccountResponse> Get(string number)
{
    var account = _service.Get(number);
    if (account is null)
        return NotFound();

    return Ok(account);
}

[HttpPost]
public ActionResult<AccountResponse> Create(NewAccount r)
{
    var created = _service.Create(r);
    return CreatedAtAction(nameof(Get),
        new { number = created.Number }, created);
}
