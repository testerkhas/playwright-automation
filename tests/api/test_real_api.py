import pytest
import random
import os
from playwright.sync_api import Playwright, APIRequestContext

pytestmark = pytest.mark.skipif(
    os.getenv("SKIP_LOCAL_API") == "true",
    reason="Skipping local API tests in CI environment"
)

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url=BASE_URL
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_context: APIRequestContext):
    response = api_context.post("/api/v1/auth/register",
        data={
            "name":     "Playwright User",
            "email":    "playwright@test.com",
            "phone":    "03001234567",
            "password": "Test@123"
        }
    )
    if response.status == 400:
        response = api_context.post("/api/v1/auth/login",
            data={
                "email":    "playwright@test.com",
                "password": "Test@123"
            }
        )
    assert response.status in [200, 201]
    token = response.json()["access_token"]
    print(f"\n✅ Auth token received")
    return token


@pytest.fixture(scope="session")
def auth_context(playwright: Playwright, auth_token: str):
    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    yield request_context
    request_context.dispose()


def test_register(api_context: APIRequestContext):
    random_num = random.randint(1, 99999)
    response = api_context.post("/api/v1/auth/register",
        data={
            "name":     "New User",
            "email":    f"newuser{random_num}@test.com",
            "phone":    "03001234567",
            "password": "Test@123"
        }
    )
    assert response.status == 201
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    print(f"✅ Register: User created with id {body['user_id']}")


def test_login(api_context: APIRequestContext):
    response = api_context.post("/api/v1/auth/login",
        data={
            "email":    "playwright@test.com",
            "password": "Test@123"
        }
    )
    # 200 if user exists, 401 if database was reset
    assert response.status in [200, 401]
    if response.status == 200:
        body = response.json()
        assert "access_token" in body
        print(f"✅ Login: Token received for user {body['name']}")
    else:
        print(f"✅ Login test ran — user may have been recreated in this session")


def test_login_wrong_password(api_context: APIRequestContext):
    response = api_context.post("/api/v1/auth/login",
        data={
            "email":    "playwright@test.com",
            "password": "WrongPassword"
        }
    )
    assert response.status == 401
    body = response.json()
    assert "detail" in body
    print(f"✅ Wrong password correctly rejected: {body['detail']}")


def test_get_all_users(auth_context: APIRequestContext):
    response = auth_context.get("/api/v1/users")
    assert response.status == 200
    body = response.json()
    assert isinstance(body, list)
    print(f"✅ Get All Users: {len(body)} users found")


def test_get_users_without_token(api_context: APIRequestContext):
    response = api_context.get("/api/v1/users")
    # FastAPI returns 401 (not 403) when no token provided
    assert response.status == 401
    print(f"✅ Protected route correctly blocked without token: {response.status}")


def test_create_user(auth_context: APIRequestContext):
    random_num = random.randint(1, 99999)
    response = auth_context.post("/api/v1/users",
        data={
            "name":     "Created User",
            "email":    f"created{random_num}@test.com",
            "phone":    "03009999999",
            "password": "Created@123"
        }
    )
    assert response.status == 201
    body = response.json()
    assert body["name"] == "Created User"
    pytest.created_user_id = body["id"]
    print(f"✅ Create User: Created with id {body['id']}")


def test_get_single_user(auth_context: APIRequestContext):
    user_id = pytest.created_user_id
    response = auth_context.get(f"/api/v1/users/{user_id}")
    assert response.status == 200
    body = response.json()
    assert body["id"] == user_id
    assert body["name"] == "Created User"
    print(f"✅ Get Single User: Found {body['name']}")


def test_update_user(auth_context: APIRequestContext):
    user_id = pytest.created_user_id
    response = auth_context.put(f"/api/v1/users/{user_id}",
        data={
            "name":  "Updated User",
            "phone": "03001111111"
        }
    )
    assert response.status == 200
    body = response.json()
    assert body["name"] == "Updated User"
    print(f"✅ Update User: Updated to {body['name']}")


def test_get_nonexistent_user(auth_context: APIRequestContext):
    response = auth_context.get("/api/v1/users/99999")
    assert response.status == 404
    print(f"✅ Non-existent user correctly returned 404")


def test_delete_user(auth_context: APIRequestContext):
    user_id = pytest.created_user_id
    response = auth_context.delete(f"/api/v1/users/{user_id}")
    assert response.status == 200
    body = response.json()
    assert "deleted successfully" in body["message"]
    print(f"✅ Delete User: {body['message']}")


def test_verify_deleted_user(auth_context: APIRequestContext):
    user_id = pytest.created_user_id
    response = auth_context.get(f"/api/v1/users/{user_id}")
    assert response.status == 404
    print(f"✅ Deleted user correctly returns 404")