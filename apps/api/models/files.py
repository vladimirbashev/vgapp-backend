from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    path = Column(String)
    createdate = Column(DateTime, default=datetime.utcnow)
    updatedate = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="files")