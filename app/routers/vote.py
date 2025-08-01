from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from ..database import SessionDep
from ..oauth2 import get_current_user
from ..models import User, Vote, Post
from typing import Annotated

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/{post_id}")
def vote_post(
    post_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )

    vote = session.exec(
        select(Vote).where(Vote.post_id == post_id, Vote.user_id == current_user.id)
    ).first()
    if not vote:
        new_vote = Vote(post_id=post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "Vote recorded successfully"}
    session.delete(vote)
    session.commit()
    return {"message": "Vote deleted"}
