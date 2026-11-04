static string Season(int month) => month switch
{
    12 or 1 or 2 => "winter",
    >= 6 and <= 8 => "summer",
    _ => "other season"
};

decimal bonus = (years, vip) switch
{
    (>= 10, true) => 0.020m,
    (>= 10, false) => 0.015m,
    _ => 0m
};
