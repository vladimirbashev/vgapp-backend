from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    password = Column(String)
    createdate = Column(DateTime, default=datetime.utcnow)
    updatedate = Column(DateTime, default=datetime.utcnow)
    bio = Column(String, nullable=True)
    image = Column(String, nullable=True)

    articles = relationship("Article", back_populates="author")
