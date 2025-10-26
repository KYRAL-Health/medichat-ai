import pymysql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Enum, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import secrets

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    access_key = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum('user', 'admin', name='user_role'), default='user')
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    submission_count = Column(Integer, default=0)

# Database setup
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

def generate_access_key():
    return secrets.token_urlsafe(32)

def add_user(access_key, role='user', email=None):
    # Input validation
    if not access_key or not isinstance(access_key, str):
        return False
    
    if role not in ['user', 'admin']:
        return False
    
    if email and not isinstance(email, str):
        return False
    
    db = SessionLocal()
    try:
        user = User(access_key=access_key, role=role, email=email)
        db.add(user)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()

def validate_key(access_key):
    if not access_key or not isinstance(access_key, str):
        return None
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.access_key == access_key, User.is_active == True).first()
        if user:
            return {
                'id': user.id,
                'role': user.role,
                'is_active': user.is_active
            }
        return None
    finally:
        db.close()

def deactivate_user(access_key):
    if not access_key or not isinstance(access_key, str):
        return False
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.access_key == access_key).first()
        if user:
            user.is_active = False
            db.commit()
            return True
        return False
    finally:
        db.close()

def reactivate_user(access_key):
    if not access_key or not isinstance(access_key, str):
        return False
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.access_key == access_key).first()
        if user:
            user.is_active = True
            db.commit()
            return True
        return False
    finally:
        db.close()

def get_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        return [{
            'id': user.id,
            'access_key': user.access_key,
            'email': user.email,
            'is_active': user.is_active,
            'role': user.role,
            'created_at': user.created_at,
            'submission_count': user.submission_count
        } for user in users]
    finally:
        db.close()

def is_admin(access_key):
    if not access_key or not isinstance(access_key, str):
        return False
    
    user_data = validate_key(access_key)
    return user_data and user_data['role'] == 'admin'

def increment_submission_count(access_key):
    if not access_key or not isinstance(access_key, str):
        return False
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.access_key == access_key).first()
        if user:
            user.submission_count += 1
            db.commit()
            return True
        return False
    finally:
        db.close()