from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import get_password_hash

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(deps.get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])

def read_users(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: User = Depends(deps.get_current_user)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    user = db.query(User).filter(User.correo == user_in.correo).first()
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system.")
    user_data = user_in.model_dump(exclude={"password"})
    user_data["hashed_password"] = get_password_hash(user_in.password)
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    elif "password" in update_data:
        del update_data["password"]
        
    for field, value in update_data.items():
        setattr(user, field, value)
        
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}/status", response_model=UserResponse)
def toggle_user_status(user_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
