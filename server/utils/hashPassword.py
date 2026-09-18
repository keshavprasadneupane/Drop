from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def comparePassword(plainPassword: str, hashedPassword: str):
    return password_hash.verify(plainPassword, hashedPassword)