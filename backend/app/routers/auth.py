from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Item
from schemas import usercreate, UserLogin, ItemCreate
from security import hash_password, verify_password, create_access_token, verify_access_token
from dependencies import get_current_user



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
    hashed_pass = hash_password(
        user.password
    )

    # Create user object
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_pass=hashed_pass
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
    
    

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        existing_user.hashed_pass
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
        

    access_token = create_access_token(
    {
        "sub": str(existing_user.id)
    }
)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    


@router.post("/items")
def create_item(
    item: ItemCreate,
    current_user = Depends(get_current_user),
    db : Session = Depends(get_db)
    ):
    
    new_item = Item(
    title=item.title,
    description=item.description,
    category=item.category,
    location=item.location,
    user_id=current_user.id
)
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
    "message": "Item created successfully",
    "item_id": new_item.id
}   