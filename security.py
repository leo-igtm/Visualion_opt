from passlib.context import CryptContext

# Se recomienda usar bcrypt, que es el estándar de facto.
# schemes define los algoritmos que se usarán. deprecated="auto" marcará los hashes antiguos para re-hashear si cambias el algoritmo.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña plana contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)