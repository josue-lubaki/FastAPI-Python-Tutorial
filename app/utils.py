from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# define function that will be used to hash passwords


def hash(password: str):
    return pwd_context.hash(password)

# method that will be used to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
