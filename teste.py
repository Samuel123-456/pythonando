import secrets


print(secrets.compare_digest('1234', '123r4'))

print(secrets.token_urlsafe(8))