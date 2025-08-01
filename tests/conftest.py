import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from sqlalchemy import URL
from fastapi import Depends
from app.config import settings
from app.main import app
from app.database import get_session
from app.oauth2 import create_access_token
from app import models
from app import utils
from datetime import date

url_object = URL.create(
    "postgresql",
    username=settings.db_user,
    password=settings.db_password,  # plain (unescaped) text
    host=settings.db_host,
    port=settings.db_port,
    database=f"{settings.db_name}_test",  # Use a test database
)

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/database_name"


@pytest.fixture(name="session")
def session_fixture():
    """Fixture to provide a database session for tests."""
    engine = create_engine(
        url_object,
        poolclass=StaticPool,
    )
    SQLModel.metadata.drop_all(engine)  # Drop all tables before creating them
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Fixture to provide a test client for the FastAPI app."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user1")
def test_user1(client: TestClient, session: Session):
    """Fixture to create a test user."""
    new_user = models.User(
        name="lalz",
        email="lalz@gmail.com",
        hashed_password=utils.get_password_hash("lalz"),
    )
    session.add(new_user)
    session.commit()
    assert new_user.id is not None
    return new_user


@pytest.fixture(name="token")
def token_fixture(client: TestClient, test_user1):
    return create_access_token(data={"sub": test_user1.email})


@pytest.fixture(name="authorized_client")
def authorized_client_fixture(client: TestClient, token: str):
    """Fixture to provide an authorized client with a token."""
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture(name="posts")
def posts_fixture(client: TestClient, session: Session, test_user1):
    """Fixture to create some test posts."""
    u1 = models.User(
        name="pradeep",
        email="pradeep@gmail.com",
        hashed_password=utils.get_password_hash("pradeep"),
    )
    p1 = models.Post(
        title="Post 1",
        subtitle="Subtitle of post 1",
        content="Content of post 1",
        img_url="https://example.com/image1.jpg",
        created_at=date.today(),
        author=u1,
    )
    p2 = models.Post(
        title="Post 2",
        subtitle="Subtitle of post 2",
        content="Content of post 2",
        img_url="https://example.com/image2.jpg",
        created_at=date.today(),
        author=test_user1,
    )
    session.add_all([p1, p2])
    session.commit()
    return [p1, p2]


@pytest.fixture(name="vote")
def test_vote_fixture(authorized_client: TestClient, session: Session, posts):
    """Fixture to create a vote."""
    post_id = posts[0].id
    response = authorized_client.post(f"/vote/{post_id}")
    assert response.status_code == 200
