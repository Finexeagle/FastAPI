from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "title": "Sample Post Title",
    #             "content": "This is the content of the sample post."
    #         }
    #     }


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
# def get_posts():
#     return {"data": my_posts}

def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return{"post": post}
    return None

@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/post/{id}")
def get_post(id: int):
    post = find_post(id)
    if post:
        return post
    return {"error": "Post not found"}  
