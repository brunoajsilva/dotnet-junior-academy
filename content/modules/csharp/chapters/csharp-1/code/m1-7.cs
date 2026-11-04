int a = 7, b = 2;
Console.WriteLine(a / b);          // 3 (integer division)
Console.WriteLine(a % b);          // 1 (remainder)
Console.WriteLine(a / (decimal)b); // 3.5

bool vip = a > 5 && b != 0;   // AND
bool any = a < 0 || b < 0;  // OR
bool inverse = !vip;          // NOT
a += 3; a++;                  // a becomes 11
