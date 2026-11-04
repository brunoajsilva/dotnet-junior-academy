string a = "Ana";
string b = "Pereira";

string c1 = a + " " + b;                  // concatenation
string c2 = string.Concat(a, " ", b);
string c3 = string.Join(", ", new[] { a, b });

var sb = new StringBuilder();            // many joins
for (int i = 0; i < 3; i++) sb.Append(i).Append(";");
string c4 = sb.ToString();               // "0;1;2;"
