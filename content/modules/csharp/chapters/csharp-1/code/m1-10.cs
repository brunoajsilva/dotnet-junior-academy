static string Classify(decimal balance)
{
    if (balance >= 1000m)
        return "high";
    else if (balance >= 300m)
        return "medium";
    else
        return "low";
}
