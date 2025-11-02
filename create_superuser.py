import getpass
from app.models import UserModel, RoleEnum
from db_config import get_db
from app.helpers import hash_password
from sqlalchemy.orm import Session

def create_superuser():
    full_name =  input("Enter full name: ")
    email =  input("enter email: ")
    password =  getpass.getpass("enter password: ")
    confirm_password =  getpass.getpass("enter confirm password: ")
    if not email or email == '':
        email = "admin@admin.com"
    if full_name and password == confirm_password:
        session = get_db()
        db = next(session)
        user_exists = db.query(UserModel).filter(UserModel.full_name == full_name).first()
        if user_exists:
            return "User already exists"
        password_hash = hash_password(password)
        user = UserModel(full_name=full_name,email=email, password=password_hash, role=RoleEnum.SUPERUSER, is_active=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        return "Superuser created successfully"
    


if __name__ == '__main__':
    create_superuser()