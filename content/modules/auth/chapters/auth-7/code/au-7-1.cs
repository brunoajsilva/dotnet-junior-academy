using Microsoft.AspNetCore.Identity;

var hasher = new PasswordHasher<object>();

// at registration: store ONLY the hash
string hash = hasher.HashPassword(null!, "Passw0rd!");
// "AQAAAAIAAYagAAAAE..."  (random salt included, different every time)

// at login: compare the typed password with the stored hash
var result = hasher.VerifyHashedPassword(null!, hash, "Passw0rd!");
bool ok = result != PasswordVerificationResult.Failed;
