from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from starlette import status

from app import models, oauth2
from app.database import get_db
from app.models import User
from app.schemas import Post, PostCreate

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/{id}", response_model=Post)
def get_posts(id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} does not exists ")
    return post


@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user), limit=10, search: Optional[str] = ''):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends((get_db)),
                current_user: User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} does not exists ")
    if post.owner_id == current_user.id:
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorised to perform requested action")


@router.put("/{id}", response_model=Post)
def update_post(id: int, new_post: PostCreate, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} does not exists ")
    if post.owner_id == current_user.id:
        post_query.update(new_post.dict(), synchronize_session=False)
        db.commit()
    return post
