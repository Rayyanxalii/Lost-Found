from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import usercreate
from security import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: usercreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    # Create user object
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    # Save to database
    db.add(new_user)
    db.commit()

    return {
        "message": "User registered successfully"
    }