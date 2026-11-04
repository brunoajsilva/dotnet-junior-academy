static decimal CalculateBonus(int customerYears)
{
    if (customerYears >= 10) return 0.015m;
    if (customerYears >= 5) return 0.010m;
    return 0m;
}

static int Add(int a, int b = 0) => a + b;

var b = CalculateBonus(6);   // 0.010
