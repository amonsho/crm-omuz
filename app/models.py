from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime
from enum import Enum


class BaseModel(DeclarativeBase):
    pass


class BlackListedToken(BaseModel):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, unique=True, nullable=False,)
    created_at = Column(DateTime, default=datetime.now)


class RoleEnum(Enum):
    SUPERUSER = "superuser"
    TEACHER = "teacher"
    STUDENT = "student"


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(200), nullable=True)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.STUDENT, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    teacher_profile = relationship("TeacherProfile", back_populates="user")
    student_profile = relationship("StudentProfile", back_populates="user")

class TeacherProfile(BaseModel):
    __tablename__ = "teacher_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True)
    bio = Column(Text, nullable=True)

    user = relationship("UserModel", back_populates="teacher_profile")
    courses = relationship("CourseModel", back_populates="teacher")

class StudentProfile(BaseModel):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True)
    enrollment_number = Column(String(100), unique=True, nullable=True)
    study_year = Column(Integer, nullable=True)

    user = relationship("UserModel", back_populates="student_profile")
    enrollments = relationship("EnrollmentModel", back_populates='student')

class CourseModel(BaseModel):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teacher_profiles.id"))

    teacher = relationship("TeacherProfile", back_populates="courses")
    enrollments = relationship("EnrollmentModel", back_populates="course")

class EnrollmentStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"

class EnrollmentModel(BaseModel):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    status = Column(SqlEnum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    enrolled_at = Column(DateTime, default=datetime.now)

    student = relationship("StudentProfile", back_populates="enrollments")
    course = relationship("CourseModel", back_populates='enrollments')
