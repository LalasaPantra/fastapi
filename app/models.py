from sqlmodel import Field, SQLModel, Column, text, DateTime, Relationship
from typing import Annotated
from datetime import datetime
from pydantic import EmailStr


class FilterParams(SQLModel):
    limit: int = 10
    offset: int = 0


class PostBase(SQLModel):
    title: Annotated[str, Field(unique=True)]
    subtitle: str
    content: str
    img_url: str


class Post(PostBase, table=True):
    __tablename__ = "posts"
    id: Annotated[int | None, Field(primary_key=True)] = None
    created_at: str
    author_id: Annotated[int, Field(foreign_key="users.id", ondelete="CASCADE")]
    author: "User" = Relationship(back_populates="posts")


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: int
    created_at: str
    author_id: int


class PostUpdate(SQLModel):
    title: str | None = None
    subtitle: str | None = None
    content: str | None = None
    img_url: str | None = None


class UserBase(SQLModel):
    name: str
    email: Annotated[EmailStr, Field(unique=True)]


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Annotated[int | None, Field(primary_key=True)] = None
    hashed_password: str = Field()
    created_at: Annotated[
        datetime | None,
        Field(
            sa_column=Column(
                DateTime(timezone=True),
                server_default=text("now()"),
                nullable=False,
            )
        ),
    ] = None
    posts: list[Post] = Relationship(back_populates="author", cascade_delete=True)


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int
    created_at: datetime


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class PostPublicWithAuthor(PostPublic):
    author: UserPublic


class UserPublicWithPosts(UserPublic):
    posts: list[PostPublic] = []


class PostOut(SQLModel):
    post: PostPublicWithAuthor
    votes: int


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: EmailStr | None = None


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    user_id: Annotated[
        int | None, Field(foreign_key="users.id", primary_key=True, ondelete="CASCADE")
    ] = None
    post_id: Annotated[
        int | None, Field(foreign_key="posts.id", primary_key=True, ondelete="CASCADE")
    ] = None
