// appsettings.json
{
  "ConnectionStrings": {
    "BankingApp": "Server=...;Database=BankingApp"
  },
  "Interest": { "MaxBonus": 0.02 }
}

// in code
var cs = builder.Configuration
    .GetConnectionString("BankingApp");
var max = builder.Configuration
    .GetValue<decimal>("Interest:MaxBonus");
