static string Season(int month)
{
    switch (month)
    {
        case 12:
        case 1:
        case 2:
            return "winter";
        case 6 or 7 or 8:
            return "summer";
        default:
            return "other season";
    }
}
