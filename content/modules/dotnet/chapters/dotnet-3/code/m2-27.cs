// Program.cs: register
builder.Services.AddScoped<IInterestCalculator,
    PromoInterest>();
builder.Services.AddScoped<AccountService>();

// the controller receives the service
public AccountsController(AccountService service)
{
    _service = service;
}
