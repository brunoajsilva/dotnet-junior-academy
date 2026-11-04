var names = new List<string> { "Ana", "Rui", "Inês" };

foreach (var name in names)
    Console.WriteLine(name);

for (int i = 0; i < names.Count; i++)
    Console.WriteLine($"{i + 1}. {names[i]}");

for (int i = 10; i > 0; i -= 3)
    Console.Write(i + " ");   // 10 7 4 1
