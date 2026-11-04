// 1. the document: built into ASP.NET Core (the template already has it)
builder.Services.AddOpenApi();

// 2. the UI: a separate package
// dotnet add package Swashbuckle.AspNetCore.SwaggerUI

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();   // serves /openapi/v1.json
    app.UseSwaggerUI(o =>
        o.SwaggerEndpoint("/openapi/v1.json", "v1"));   // /swagger
}
