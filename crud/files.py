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


def create_user_file(db: Session, file: schemas.FileCreate, user_id: int):
    db_article = models.File(**file.dict(), user_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
