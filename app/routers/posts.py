from fastapi import Body, HTTPException, APIRouter, Depends, Query
from .. import models as model
from ..database import SessionDep
from typing import Annotated
from sqlmodel import select, func
from datetime import date
from ..oauth2 import get_current_user

router = APIRouter(tags=["posts"])


@router.get("/", response_model=list[model.PostOut])
def get_all_posts(
    session: SessionDep, filter_query: Annotated[model.FilterParams, Query()]
):
    stmt = (
        select(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True)
        .group_by(model.Post.id)
        .order_by(model.Post.id)
        .limit(filter_query.limit)
        .offset(filter_query.offset)
    )
    # stmt = select(model.Post)
    posts = session.exec(stmt).all()
    results = []
    # import ipdb

    # ipdb.set_trace()
    for post, votes in posts:
        results.append(model.PostOut(post=post, votes=votes))
    return results


@router.get("/post/{post_id}", response_model=model.PostPublicWithAuthor)
def show_post(post_id: int, session: SessionDep):
    post = session.get(model.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/new-post", response_model=model.PostPublic)
def create_post(
    post: Annotated[model.PostCreate, Body()],
    session: SessionDep,
    current_user: Annotated[model.User, Depends(get_current_user)],
):
    extra_data = {
        "created_at": date.today().strftime("%B %d, %Y"),
        "author_id": current_user.id,
    }
    new_post = model.Post.model_validate(post, update=extra_data)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.patch("/update-post/{post_id}", response_model=model.PostPublic)
def update_post(
    post_id: int,
    post: model.PostUpdate,
    session: SessionDep,
    current_user: Annotated[model.User, Depends(get_current_user)],
):
    db_post = session.get(model.Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this post"
        )
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.delete("/delete-post/{post_id}")
def delete_post(
    post_id: int,
    session: SessionDep,
    current_user: Annotated[model.User, Depends(get_current_user)],
):
    post = session.get(model.Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this post"
        )
    session.delete(post)
    session.commit()
    return {"message": "Post deleted successfully"}
