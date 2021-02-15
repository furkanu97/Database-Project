from passlib.hash import pbkdf2_sha256 as hasher

DEBUG = True
PORT = 8080
SECRET_KEY = "secret"
WTF_CSRF_ENABLED = True

password = "adminpw"
hashed = hasher.hash(password)

PASSWORDS = {
    "admin": hashed,
}

ADMIN_USERS = ["admin"]