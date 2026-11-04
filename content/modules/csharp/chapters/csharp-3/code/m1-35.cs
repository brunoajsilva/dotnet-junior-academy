// blocks the thread for 2 seconds
Thread.Sleep(2000);

// frees the thread while waiting
await Task.Delay(2000);

// real example: HTTP call
using var http = new HttpClient();
string json = await http
    .GetStringAsync("https://example.com/quote");
Console.WriteLine(json.Length);
