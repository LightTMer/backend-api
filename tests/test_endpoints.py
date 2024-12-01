import pytest
from fastapi.testclient import TestClient
from app.__main__ import app
from app.models import User, Group
from app.settings import app_settings

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_test_data():
    user1 = User(user_id=1, name="User1", sex="male", home_town="TownA").save()
    user2 = User(user_id=2, name="User2", sex="female", home_town="TownB").save()
    group1 = Group(group_id=1, name="Group1").save()

    
    user1.follows.connect(user2)
    user1.subscribes.connect(group1)

    yield user1, user2, group1


    user1.delete()
    user2.delete()
    group1.delete()


# GET /users
def test_get_users(setup_test_data):
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  
    assert all("user_id" in item for item in data)


# GET /users/{user_id}
def test_get_user(setup_test_data):
    user1, user2, _ = setup_test_data
    response = client.get(f"/users/{user1.user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user1.user_id
    assert "follows" in data
    assert "subscribes" in data
    assert any(f["user_id"] == user2.user_id for f in data["follows"])


# POST /users
def test_create_user():
    payload = {
        "user_id": 3,
        "name": "User3",
        "sex": "male",
        "home_town": "TownC",
        "follows": [],
        "subscribes": [],
    }
    response = client.post(
        "/users",
        headers={"Authorization": f"Bearer {app_settings.ACCESS_TOKEN}"},
        json=payload,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == payload["user_id"]
    User.nodes.get(user_id=payload["user_id"]).delete()  


# DELETE /users/{user_id}
def test_delete_user(setup_test_data):
    user1, _, _ = setup_test_data
    response = client.delete(
        f"/users/{user1.user_id}",
        headers={"Authorization": f"Bearer {app_settings.ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert User.nodes.get_or_none(user_id=user1.user_id) is None


# GET /groups
def test_get_groups(setup_test_data):
    response = client.get("/groups")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1 
    assert all("group_id" in item for item in data)


# GET /groups/{group_id}
def test_get_group(setup_test_data):
    _, _, group1 = setup_test_data
    response = client.get(f"/groups/{group1.group_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == group1.group_id
    assert "subscribers" in data
    assert any(u["user_id"] == 1 for u in data["subscribers"])


# POST /groups
def test_create_group():
    payload = {"group_id": 2, "name": "Group2", "subscribers": []}
    response = client.post(
        "/groups",
        json=payload,
        headers={"Authorization": f"Bearer {app_settings.ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == payload["group_id"]
    Group.nodes.get(group_id=payload["group_id"]).delete() 


# DELETE /groups/{group_id}
def test_delete_group(setup_test_data):
    _, _, group1 = setup_test_data
    response = client.delete(
        f"/groups/{group1.group_id}",
        headers={"Authorization": f"Bearer {app_settings.ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert Group.nodes.get_or_none(group_id=group1.group_id) is None
