from typing import Optional

from fastapi import FastAPI, HTTPException, Response, Depends
from pydantic import BaseModel
from starlette import status
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
my_posts = []

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database conn successfull")
except:
    print("DB connection failed")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute("SELECT * from posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} does not exists ")
    return {"message": post}


@app.get("/posts")
def get_posts():
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts")
def create_post(post: Post):
    cursor.execute("INSERT INTO posts(title, content, published) values(%s, %s, %s) RETURNING *",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": new_post}


def find_post(id: int):
    for idx, post in enumerate(my_posts):
        if post['id'] == id:
            return idx
    return None


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID:{id} does not exists ")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} Id does not exists")
    return {'message': updated_post}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {'message' :'connect sqlalchemy'}