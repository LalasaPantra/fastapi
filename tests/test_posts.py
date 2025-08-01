from fastapi.testclient import TestClient
from app import models

# from app.oauth2 import create_access_token


def test_get_all_posts(client: TestClient, posts):
    parameters = {
        "limit": 10,
        "offset": 0,
    }
    response = client.get("/", params=parameters)
    posts_response = [models.PostOut.model_validate(post) for post in response.json()]
    assert len(posts_response) == len(posts)
    assert response.status_code == 200


def test_show_post(client: TestClient, posts):
    response = client.get(f"/post/{posts[0].id}")
    post = models.PostPublicWithAuthor.model_validate(response.json())
    assert post.id == posts[0].id
    assert response.status_code == 200


def test_create_post(authorized_client: TestClient):
    body = {
        "title": "New Post",
        "subtitle": "This is a subtitle for the new post.",
        "content": "This is a new post.",
        "img_url": "https://example.com/image.jpg",
    }
    response = authorized_client.post("/new-post", json=body)
    new_post = models.PostPublic.model_validate(response.json())
    assert new_post.id is not None
    assert response.status_code == 200


def test_create_post_unauthorized(client: TestClient):
    # token = create_access_token(data={"sub": test_user1.email})
    # headers = {"Authorization": f"Bearer {token}"}
    body = {
        "title": "New Post",
        "subtitle": "This is a subtitle for the new post.",
        "content": "This is a new post.",
        "img_url": "https://example.com/image.jpg",
    }
    response = client.post("/new-post", json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_update_post(authorized_client: TestClient, posts):
    post_id = posts[1].id
    body = {
        "title": "Updated Post",
        "subtitle": "This is an updated subtitle.",
        "content": "This is the updated content.",
        # "img_url": "https://example.com/updated_image.jpg",
    }
    response = authorized_client.patch(f"/update-post/{post_id}", json=body)
    updated_post = models.PostPublic.model_validate(response.json())
    assert updated_post.id == post_id
    assert updated_post.title == body["title"]
    assert response.status_code == 200


def test_update_post_diff_user(authorized_client: TestClient, posts):
    post_id = posts[0].id
    body = {
        "title": "Updated Post",
    }
    response = authorized_client.patch(f"/update-post/{post_id}", json=body)
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized to update this post"}


def test_delete_post(authorized_client: TestClient, posts):
    post_id = posts[1].id
    response = authorized_client.delete(f"/delete-post/{post_id}")
    assert response.status_code == 200
