string? email = null;      // ? = nullable
int? age = null;

int n = email?.Length ?? 0;   // ?. e ??
email ??= "no e-mail";       // assigns only if null
Console.WriteLine(email);     // no e-mail

int years = age ?? 0;       // default value
