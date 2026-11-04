[ApiController]
[Route("api/accounts")]
public class AccountsController : ControllerBase
{
    [HttpGet]                     // GET api/accounts
    public IActionResult List() { ... }

    [HttpGet("{number}")]         // GET api/accounts/AC-001
    public IActionResult Get(string number) { ... }

    [HttpPost]                    // POST api/accounts
    public IActionResult Create(NewAccount r) { ... }
}
