import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_status_returns_ok(client: AsyncClient) -> None:
    resp = await client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_tasks_returns_list(client: AsyncClient) -> None:
    resp = await client.get("/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "task_id" in data[0]
    assert "title" in data[0]
    assert "status" in data[0]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_report_returns_productivity_report(client: AsyncClient) -> None:
    resp = await client.get("/report")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "total_hours_spent" in data
    assert "completion_rate" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_message_dict(client: AsyncClient) -> None:
    payload = {
        "task_id": 0,
        "title": "New test task",
        "status": "pending",
        "hours_spent": 1.5,
    }
    resp = await client.post("/log_task", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "logged successfully" in data["message"]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_invalid_payload_returns_422(client: AsyncClient) -> None:
    resp = await client.post("/log_task", json={"title": "Missing required fields"})
    assert resp.status_code == 422
