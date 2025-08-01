from fastapi.testclient import TestClient


def test_vote_post(authorized_client: TestClient, posts):
    post_id = posts[0].id
    response = authorized_client.post(f"/vote/{post_id}")
    assert response.status_code == 200


def test_vote_remove(authorized_client: TestClient, posts, vote):
    post_id = posts[0].id
    response = authorized_client.post(f"/vote/{post_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Vote deleted"}
