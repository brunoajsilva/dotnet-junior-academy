# the client joins "user:password" and encodes it in base64
echo -n 'ana@example.com:Passw0rd!' | base64
# YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==

# the header sent on EVERY request
Authorization: Basic YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==

# base64 is an encoding, not encryption: anyone can reverse it
echo 'YW5hQGV4YW1wbGUuY29tOlBhc3N3MHJkIQ==' | base64 -d
# ana@example.com:Passw0rd!

# curl does the same with -u
curl -u 'ana@example.com:Passw0rd!' https://localhost:5001/api/dashboard
