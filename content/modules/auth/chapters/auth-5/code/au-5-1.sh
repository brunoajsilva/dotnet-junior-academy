dotnet new webapi --use-controllers -n AuthLab
cd AuthLab

dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer

# remove the template sample (WeatherForecast) and keep only Program.cs
