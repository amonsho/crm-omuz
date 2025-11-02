from passlib.hash import pbkdf2_sha256

def hash_password(password:str):
    password_hash = pbkdf2_sha256.hash(password)
    return password_hash

def verify_password(password:str, password_hash:str):
    return pbkdf2_sha256.verify(password, password_hash)