app.Use(async (context, next) =>
{
    var sw = Stopwatch.StartNew();

    await next();

    var ms = sw.ElapsedMilliseconds;
    Console.WriteLine($"{context.Request.Path}: {ms} ms");
});
