// Program.cs, inside AddJwtBearer
options.TokenValidationParameters = new TokenValidationParameters
{
    // ...same as before, plus:
    NameClaimType = "name",    // User.Identity.Name reads this claim
    RoleClaimType = "role"     // [Authorize(Roles = ...)] and User.IsInRole read this claim
};

// AdminController.cs
[ApiController]
[Route("api/admin")]
public class AdminController : ControllerBase
{
    [Authorize(Roles = "Manager")]
    [HttpGet("customers")]
    public IActionResult ListCustomers() => Ok(new[] { "Ana Pereira", "Rui Costa" });
}
