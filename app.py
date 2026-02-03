from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Blog Post API")


class BlogPostCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)


class BlogPost(BlogPostCreate):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


posts: Dict[int, BlogPost] = {}
next_id = 1


@app.get("/posts", response_model=List[BlogPost])
def list_posts() -> List[BlogPost]:
    return list(posts.values())


@app.post("/posts", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
def create_post(post: BlogPostCreate) -> BlogPost:
    global next_id
    created = BlogPost(
        id=next_id,
        title=post.title,
        content=post.content,
        author=post.author,
        created_at=datetime.utcnow(),
    )
    posts[next_id] = created
    next_id += 1
    return created


@app.get("/posts/{post_id}", response_model=BlogPost)
def get_post(post_id: int) -> BlogPost:
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{post_id}", response_model=BlogPost)
def update_post(post_id: int, update: BlogPostCreate) -> BlogPost:
    post = posts.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    updated = post.copy(
        update={
            "title": update.title,
            "content": update.content,
            "author": update.author,
            "updated_at": datetime.utcnow(),
        }
    )
    posts[post_id] = updated
    return updated


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int) -> None:
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts[post_id]

