// Program.cs
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("CanReviewLoans", p => p
        .RequireRole("Manager")
        .RequireClaim("department", "Credit"))
    .AddPolicy("VerifiedEmail", p => p
        .RequireClaim("email_verified", "true"));

// LoansController.cs
[Authorize(Policy = "CanReviewLoans")]
[HttpPost("{id}/approve")]
public IActionResult Approve(int id) => NoContent();
