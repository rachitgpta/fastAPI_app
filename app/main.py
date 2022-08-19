
from fastapi import FastAPI, HTTPException, Response, Depends
from starlette import status
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
from app.schemas import PostCreate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
my_posts = []


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} does not exists ")
    return {"message": post}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends((get_db))):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": new_post}


def find_post(id: int):
    for idx, post in enumerate(my_posts):
        if post['id'] == id:
            return idx
    return None


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} does not exists ")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if old_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Id does not exists")
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()
    return {'message': post_query.first()}
