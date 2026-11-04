int years = 12;
string kind = years >= 10 ? "loyal" : "new";   // ternary

object value = "AC-001";
if (value is string s && s.StartsWith("AP"))
    Console.WriteLine(s);                  // is + variable

bool ok = years is >= 5 and < 20;         // range
string name = nameof(years);              // "years"
