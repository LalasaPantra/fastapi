from fastapi import Body, HTTPException, APIRouter, Depends
from .. import models as model, utils
from ..database import SessionDep
from typing import Annotated
from sqlmodel import select

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=model.UserPublic)
def register_user(
    user: Annotated[model.UserCreate, Body()],
    session: SessionDep,
):
    existing_user = session.exec(
        select(model.User).where(model.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = utils.get_password_hash(user.password)
    extra_data = {
        "hashed_password": hashed_password,
    }
    new_user = model.User.model_validate(user, update=extra_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=model.UserPublicWithPosts)
def get_user(user_id: int, session: SessionDep):
    user = session.get(model.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
