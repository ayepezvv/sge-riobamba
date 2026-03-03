import re

path = "app/api/routes/users.py"
with open(path, "r") as f:
    content = f.read()

content = content.replace("UserCreate, UserResponse", "UserCreate, UserResponse, UserUpdate")

new_routes = """
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
"""

with open(path, "a") as f:
    f.write(new_routes)
