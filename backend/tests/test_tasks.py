async def test_health_reports_ok(client):
    response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_a_task_can_be_created_completed_and_removed(client):
    created = await client.post("/api/tasks", json={"title": "Write the README"})

    assert created.status_code == 201
    task = created.json()
    assert task["title"] == "Write the README"
    assert task["done"] is False

    listed = await client.get("/api/tasks")

    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [task["id"]]

    completed = await client.patch(f"/api/tasks/{task['id']}", json={"done": True})

    assert completed.status_code == 200
    assert completed.json()["done"] is True

    removed = await client.delete(f"/api/tasks/{task['id']}")

    assert removed.status_code == 204

    remaining = await client.get("/api/tasks")

    assert remaining.json() == []


async def test_unknown_task_is_not_found(client):
    response = await client.patch("/api/tasks/does-not-exist", json={"done": True})

    assert response.status_code == 404


async def test_timestamps_keep_their_timezone_across_reads(client):
    created = await client.post("/api/tasks", json={"title": "Check the clock"})
    listed = await client.get("/api/tasks")

    assert created.json()["created_at"].endswith("Z")
    assert listed.json()[0]["created_at"] == created.json()["created_at"]
