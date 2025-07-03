import bcrypt

print(bcrypt.hashpw(b"admin1234", bcrypt.gensalt()).decode())
