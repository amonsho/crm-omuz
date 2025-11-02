from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import UserModel, BlackListedToken, RoleEnum, TeacherProfile, StudentProfile
from db_config import get_db
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.schemas import UserCreate, UserLoginSchema
from app.helpers import hash_password, verify_password


router = APIRouter(prefix='/auth', tags=["Authentication"])


@router.post("register")
async def register_user(user:UserCreate, db:Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")
    
    new_user = UserModel(full_name=user.full_name, email= user.email,password = hash_password(user.password) ,role = user.role, is_active = True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role == RoleEnum.TEACHER:
        teacher_profile = TeacherProfile(user_id = new_user.id)
        db.add(teacher_profile)
    elif user.role == RoleEnum.STUDENT:
        student_profile = StudentProfile(user_id = new_user.id)
        db.add(student_profile)
    db.commit()
