eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwibmFtZSI6IkFuYSJ9.kD3x...

# 1. header (base64url)
{ "alg": "HS256", "typ": "JWT" }

# 2. payload = the claims (base64url)
{
  "sub": "1",
  "name": "Ana Pereira",
  "role": "Customer",
  "iss": "AuthLab",
  "aud": "AuthLab.Clients",
  "iat": 1793690000,
  "exp": 1793693600
}

# 3. signature
HMACSHA256( base64url(header) + "." + base64url(payload), secretKey )
