from sqlalchemy import Column, String, DateTime, Integer,Text, ForeignKey
from datetime import datetime

from sqlalchemy.orm import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    hashed_pass = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    
class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)

    description = Column(Text)

    status = Column(String, nullable=False)

    location = Column(String, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )