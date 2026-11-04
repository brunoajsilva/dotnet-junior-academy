var name = "Ana";
decimal balance = 320.5m;

string s1 = $"Hello, {name}!";
string s2 = $"With interest: {balance * 1.02m}";
string s3 = $"{name.ToUpper()} has {name.Length} letters";
string s4 = $"Level: {(balance > 300m ? "alto" : "baixo")}";

string json = $$"""{ "name": "{{name}}" }""";
