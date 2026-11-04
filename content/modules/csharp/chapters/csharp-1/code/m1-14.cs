int attempts = 0;
while (attempts < 5)
{
    attempts++;
    if (attempts == 2) continue;   // next round
    if (attempts == 4) break;      // exits the loop
    Console.WriteLine(attempts);
}

string? line;
do
{
    line = Console.ReadLine();
} while (string.IsNullOrWhiteSpace(line));
