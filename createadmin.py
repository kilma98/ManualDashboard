from core.db import SessionLocal
from models.user import User
from models.measurement import Measurement
from models.threshold import Threshold
from core.security import hash_password
from passlib.context import CryptContext

# Password hashing setup (same as in FastAPI tutorials)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



def create_admin():
    db = SessionLocal()
    try:
        username = "skander"
        password = "admin123"
        role = "admin"

        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            password_hash=hashed_password,
            role=role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ Admin created: {new_user.username}")

    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
