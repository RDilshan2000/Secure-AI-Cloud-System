from passlib.context import CryptContext

#use Hashing Algorithm (bcrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

#input the Password Chenge the hash
def get_password_hash(password):
    return pwd_context.hash(password)

#Check the password(enter user password and database password maching the hash)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
