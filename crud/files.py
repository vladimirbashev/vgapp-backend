from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import files as schemas
from models import files as models


def get_files(db: Session, user_id: int = None, skip: int = 0, limit: int = 10):
    query = db.query(models.File)
    if user_id:
        query = query.filter(models.File.user_id == user_id)
    return query.order_by(models.File.id).offset(skip).limit(limit).all()


def get_files_count(db: Session, user_id: int = None):
    query = db.query(models.File)
    if user_id:
        query = query.filter(models.File.user_id == user_id)
    return query.count()


def create_user_file(db: Session, user_id: int, path: str):
    db_file = models.File(user_id=user_id, path=path)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, file_id: int):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="Hero not found")
    db.delete(file)
    db.commit()
    return {"id": file_id}
