import pytest
from playwright.sync_api import Playwright, APIRequestContext

# Setup API context (runs before each test)
@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield request_context
    request_context.dispose()


# ✅ GET - Fetch a single user
def test_get_user(api_request_context: APIRequestContext):
    response = api_request_context.get("/users/1")
    
    # Check status code
    assert response.status == 200
    
    # Parse response body
    body = response.json()
    
    # Check data
    assert body["id"] == 1
    assert body["name"] == "Leanne Graham"
    assert body["email"] == "Sincere@april.biz"
    
    print(f"✅ GET User: {body['name']}")


# ✅ GET - Fetch all posts
def test_get_all_posts(api_request_context: APIRequestContext):
    response = api_request_context.get("/posts")
    
    assert response.status == 200
    
    body = response.json()
    
    # Should return 100 posts
    assert len(body) == 100
    
    print(f"✅ GET All Posts: {len(body)} posts found")


# ✅ POST - Create a new post
def test_create_post(api_request_context: APIRequestContext):
    response = api_request_context.post("/posts",
        data={
            "title": "My First Post",
            "body": "This is the post body",
            "userId": 1
        }
    )
    
    # 201 = Created successfully
    assert response.status == 201
    
    body = response.json()
    assert body["title"] == "My First Post"
    assert body["userId"] == 1
    
    print(f"✅ POST Created: {body['title']} with id {body['id']}")


# ✅ PUT - Update a post
def test_update_post(api_request_context: APIRequestContext):
    response = api_request_context.put("/posts/1",
        data={
            "title": "Updated Title",
            "body": "Updated body",
            "userId": 1
        }
    )
    
    assert response.status == 200
    
    body = response.json()
    assert body["title"] == "Updated Title"
    
    print(f"✅ PUT Updated: {body['title']}")


# ✅ DELETE - Delete a post
def test_delete_post(api_request_context: APIRequestContext):
    response = api_request_context.delete("/posts/1")
    
    # 200 = Deleted successfully
    assert response.status == 200
    
    print("✅ DELETE: Post deleted successfully")