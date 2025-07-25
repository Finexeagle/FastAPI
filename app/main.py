from fastapi import FastAPI
from fastapi import Body
from fastapi import Response, status, HTTPException
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
def get_posts():
     return {"data": my_posts}

def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return{"post": post}
    return None

def get_post_index(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        
    return None

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/post/latest")
def get_latest_posts():
    post_dict = my_posts[-1]
    return {"data": post_dict}


@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"data": post}


@app.delete("/post/{id}")
def delete_post(id: int):
    post_index = get_post_index(id)
    if post_index is not None:
        my_posts.pop(post_index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail="Post with id doesent Exist")
    
@app.put("/post/{id}")
def update_post(id: int, updated_post: Post):
    post = find_post(id)
    post_index = get_post_index(id)
    if post_index is not None:
        updated_post = updated_post.dict()
        updated_post['id'] = post['post']['id']
        my_posts[post_index] = updated_post
        return {f"Post {updated_post['id']} updated": my_posts[post_index]}
    else:
        raise HTTPException(status_code=404, detail="Post with id doesent Exist")

    
    
