# header
{ "alg": "HS256", "typ": "JWT" }

# payload (the claims)
{
  "sub": "1",
  "email": "ana@example.com",
  "name": "Ana Pereira",
  "exp": 1793700000,
  "iss": "BankingApp",
  "aud": "BankingApp.Clients"
}

# signature = HMACSHA256(header + "." + payload, Jwt:Key)
# anyone can READ the payload (base64): never put secrets in it
