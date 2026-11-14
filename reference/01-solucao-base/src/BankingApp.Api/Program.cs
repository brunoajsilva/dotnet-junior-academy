using BankingApp.Api.Middleware;
using BankingApp.Api.Responses;
using BankingApp.Application;
using BankingApp.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers()
    .ConfigureApiBehaviorOptions(o =>
        o.InvalidModelStateResponseFactory = ValidationResponse.Create);   // invalid DTO -> 200 + errors
builder.Services.AddOpenApi();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();   // first: catches everything below

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();                        // /openapi/v1.json
    app.UseSwaggerUI(o => o.SwaggerEndpoint("/openapi/v1.json", "v1"));   // /swagger
}

app.UseHttpsRedirection();
app.MapControllers();

app.Run();
