import pytest
from playwright.sync_api import Playwright, APIRequestContext, Page, expect


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    request_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield request_context
    request_context.dispose()


# ============================================
# TEST 1 - Create via API, Verify Response
# ============================================
def test_create_and_verify_post(api_request_context: APIRequestContext):

    # STEP 1: Create a post via API
    create_response = api_request_context.post("/posts",
        data={
            "title": "Automation Post",
            "body": "Created by Playwright",
            "userId": 1
        }
    )
    assert create_response.status == 201
    created_post = create_response.json()
    print(f"✅ STEP 1: Post created with id: {created_post['id']}")

    # STEP 2: Verify the response data is correct
    # (jsonplaceholder is fake - doesn't actually save, so we verify response only)
    assert created_post["title"] == "Automation Post"
    assert created_post["userId"] == 1
    print(f"✅ STEP 2: Response data verified correctly")

    # STEP 3: Fetch a real existing post (id 1-100 always exist)
    get_response = api_request_context.get("/posts/1")
    assert get_response.status == 200
    post = get_response.json()
    assert post["id"] == 1
    print(f"✅ STEP 3: Fetched real post: '{post['title']}'")


# ============================================
# TEST 2 - API Setup + UI Verification
# ============================================
def test_api_then_ui(api_request_context: APIRequestContext, page: Page):

    # STEP 1: Get user data via API
    response = api_request_context.get("/users/1")
    assert response.status == 200
    user = response.json()
    print(f"✅ STEP 1: Got user from API: {user['name']}")

    # STEP 2: Open website in browser
    page.goto("https://the-internet.herokuapp.com/login")
    print("✅ STEP 2: Browser opened login page")

    # STEP 3: Fill form and login
    page.fill("#username", "tomsmith")
    page.fill("#password", "SuperSecretPassword!")
    page.click("button[type='submit']")
    print("✅ STEP 3: Filled and submitted form")

    # STEP 4: Verify UI shows success
    expect(page.locator(".flash.success")).to_be_visible()
    print("✅ STEP 4: UI verified login success!")


# ============================================
# TEST 3 - Full CRUD Flow (using real IDs)
# ============================================
def test_full_crud_flow(api_request_context: APIRequestContext):
    print("\n--- Starting Full CRUD Flow ---")

    # CREATE - verify response data only (fake API doesn't save)
    create_res = api_request_context.post("/posts",
        data={"title": "Test Post", "body": "Test Body", "userId": 1}
    )
    assert create_res.status == 201
    post = create_res.json()
    assert post["title"] == "Test Post"
    print(f"✅ CREATE: Post '{post['title']}' created and verified")

    # READ - use a real existing post (1-100)
    read_res = api_request_context.get("/posts/1")
    assert read_res.status == 200
    real_post = read_res.json()
    print(f"✅ READ: Fetched post '{real_post['title']}'")

    # UPDATE - update a real existing post
    update_res = api_request_context.put("/posts/1",
        data={"title": "Updated Post", "body": "Updated Body", "userId": 1}
    )
    assert update_res.status == 200
    updated = update_res.json()
    assert updated["title"] == "Updated Post"
    print(f"✅ UPDATE: Post updated to '{updated['title']}'")

    # DELETE - delete a real existing post
    delete_res = api_request_context.delete("/posts/1")
    assert delete_res.status == 200
    print(f"✅ DELETE: Post deleted successfully")
    print("--- Full CRUD Flow Complete! ---")