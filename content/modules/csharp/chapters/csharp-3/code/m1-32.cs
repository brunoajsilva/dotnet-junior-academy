try
{
    Console.WriteLine(100 / int.Parse(text));
}
catch (FormatException)
{ Console.WriteLine("Not a number"); }
catch (DivideByZeroException)
{ Console.WriteLine("Zero!"); }
catch (Exception ex)
{ Console.WriteLine(ex.Message); }
finally
{ Console.WriteLine("Done"); }   // always runs
