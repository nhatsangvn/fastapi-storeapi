import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/post",
        json={"body": body},
    )
    return response.json()


async def create_comment(body: str, post_id: int, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": post_id},
    )
    return response.json()


# used for referenced later
@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    return await create_comment("Test Comment", 0, async_client)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    body = "Test Post"
    response = await async_client.post(
        "/post",
        json={"body": body},
    )
    assert response.status_code == 201
    assert {"id": 0, "body": "Test Post"}.items() <= response.json().items()


# note that we pass created_post as argument so it will be created first
@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "Test Comment"

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]},
    )
    assert response.status_code == 201
    assert {
        "id": 0,
        "body": "Test Comment",
        "post_id": 0,
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post(
        "/post",
        json={},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_comment_missing_data(async_client: AsyncClient):
    response = await async_client.post(
        "/comment",
        json={},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_post(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_get_comment_on_post(async_client: AsyncClient, created_comment: dict):
    post_id = created_comment["post_id"]

    response = await async_client.get(f"/post/{post_id}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comment_on_post_empty(async_client: AsyncClient, created_post: dict):
    post_id = created_post["id"]

    response = await async_client.get(f"/post/{post_id}/comment")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comment(async_client: AsyncClient, created_post: dict, created_comment: dict):
    post_id = created_post["id"]

    response = await async_client.get(f"/post/{post_id}")

    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comment": [created_comment]
    }

@pytest.mark.anyio
async def test_get_comment_on_mising_post(async_client: AsyncClient):
    response = await async_client.get(f"/post/-1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Post not found'}
