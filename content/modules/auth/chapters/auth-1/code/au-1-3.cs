var app = builder.Build();

app.UseHttpsRedirection();

app.UseAuthentication();   // 1. who are you?  Reads the credentials and builds the User
app.UseAuthorization();    // 2. can you do this?  Checks [Authorize] against the User

app.MapControllers();
app.Run();
