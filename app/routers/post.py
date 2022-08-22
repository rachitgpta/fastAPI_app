from typing import List

from fastapi import Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from app.schemas import Post, PostCreate

router = APIRouter()

@router.get("/posts/{id}", response_model=Post)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} does not exists ")
    return post


@router.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends((get_db))):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} does not exists ")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if old_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Id does not exists")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
