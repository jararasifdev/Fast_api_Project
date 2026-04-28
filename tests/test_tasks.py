import pytest
from datetime import date

def test_create_task(client, auth_headers):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    response = client.post("/tasks/", json=task_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["status"] == task_data["status"]
    assert data["priority"] == task_data["priority"]
    assert "id" in data
    assert "created_at" in data

def test_create_task_unauthorized(client):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 401

def test_get_task(client, auth_headers):
    # Create a task first
    task_data = {
        "title": "Get Test Task",
        "description": "Test Description",
        "status": "todo",
        "priority": "high",
        "due_date": "2024-12-31"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]

    # Get the task
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_get_task_not_found(client, auth_headers):
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_get_task_unauthorized(client):
    response = client.get("/tasks/1")
    assert response.status_code == 401

def test_update_task(client, auth_headers):
    # Create a task first
    task_data = {
        "title": "Update Test Task",
        "description": "Original Description",
        "status": "todo",
        "priority": "low",
        "due_date": "2024-12-31"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "status": "in_progress",
        "priority": "high"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]
    assert data["priority"] == update_data["priority"]

def test_update_task_not_found(client, auth_headers):
    update_data = {
        "title": "Updated Task",
        "status": "in_progress"
    }
    response = client.put("/tasks/999", json=update_data, headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_delete_task(client, auth_headers):
    # Create a task first
    task_data = {
        "title": "Delete Test Task",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"msg": "Task Deleted Succesfully"}

    # Verify it's deleted
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_task_not_found(client, auth_headers):
    response = client.delete("/tasks/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_get_tasks_pagination(client, auth_headers):
    # Create multiple tasks
    for i in range(5):
        task_data = {
            "title": f"Task {i}",
            "description": f"Description {i}",
            "status": "todo",
            "priority": "medium",
            "due_date": "2024-12-31"
        }
        client.post("/tasks/", json=task_data, headers=auth_headers)

    # Get first page
    response = client.get("/tasks/?page=1&limit=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total_tasks"] == 5
    assert data["total_pages"] == 3
    assert len(data["data"]) == 2

def test_get_tasks_filtering(client, auth_headers):
    # Create tasks with different statuses
    tasks_data = [
        {
            "title": "Todo Task",
            "description": "Todo Description",
            "status": "todo",
            "priority": "medium",
            "due_date": "2024-12-31"
        },
        {
            "title": "Done Task",
            "description": "Done Description",
            "status": "done",
            "priority": "high",
            "due_date": "2024-12-31"
        }
    ]

    for task_data in tasks_data:
        client.post("/tasks/", json=task_data, headers=auth_headers)

    # Filter by status
    response = client.get("/tasks/?status=done", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["status"] == "done"

def test_get_tasks_search(client, auth_headers):
    # Create tasks
    tasks_data = [
        {
            "title": "Python Task",
            "description": "Learn Python",
            "status": "todo",
            "priority": "medium",
            "due_date": "2024-12-31"
        },
        {
            "title": "Java Task",
            "description": "Learn Java",
            "status": "todo",
            "priority": "high",
            "due_date": "2024-12-31"
        }
    ]

    for task_data in tasks_data:
        client.post("/tasks/", json=task_data, headers=auth_headers)

    # Search by title
    response = client.get("/tasks/?search=Python", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert "Python" in data["data"][0]["title"]

def test_add_tag_to_task(client, auth_headers):
    # Create a task
    task_data = {
        "title": "Task with Tag",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = task_response.json()["id"]

    # Create a tag
    tag_data = {"name": "Test Tag"}
    tag_response = client.post("/tags/", json=tag_data)
    tag_id = tag_response.json()["id"]

    # Add tag to task
    response = client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Tag added to task successfully"}

def test_add_tag_to_task_not_found(client, auth_headers):
    # create a task first
    task_data = {
        "title": "Test Task",
        "description": "Test",
        "status": "todo",
        "priority": "low",
        "due_date": "2026-05-01"
    }

    task_res = client.post("/tasks", json=task_data, headers=auth_headers)
    task_id = task_res.json()["id"]

    # now use valid task, invalid tag
    response = client.post(f"/tasks/{task_id}/tags/999", headers=auth_headers)

    assert response.status_code == 404
    assert "Tag not found" in response.json()["detail"]

def test_add_nonexistent_tag_to_task(client, auth_headers):
    # Create a task
    task_data = {
        "title": "Task",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = task_response.json()["id"]

    response = client.post(f"/tasks/{task_id}/tags/999", headers=auth_headers)
    assert response.status_code == 404
    assert "Tag not found" in response.json()["detail"]

def test_add_duplicate_tag_to_task(client, auth_headers):
    # Create a task
    task_data = {
        "title": "Task with Duplicate Tag",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = task_response.json()["id"]

    # Create a tag
    tag_data = {"name": "Duplicate Tag"}
    tag_response = client.post("/tags/", json=tag_data)
    tag_id = tag_response.json()["id"]

    # Add tag first time
    client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)

    # Add same tag again
    response = client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)
    assert response.status_code == 400
    assert "Tag already added to task" in response.json()["detail"]

def test_get_tasks_by_tag(client, auth_headers):
    # Create a tag
    tag_data = {"name": "Filter Tag"}
    tag_response = client.post("/tags/", json=tag_data)
    tag_id = tag_response.json()["id"]

    # Create tasks
    task_data1 = {
        "title": "Task 1",
        "description": "Test Description 1",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_data2 = {
        "title": "Task 2",
        "description": "Test Description 2",
        "status": "done",
        "priority": "high",
        "due_date": "2024-12-31"
    }

    task1_response = client.post("/tasks/", json=task_data1, headers=auth_headers)
    task1_id = task1_response.json()["id"]
    task2_response = client.post("/tasks/", json=task_data2, headers=auth_headers)
    task2_id = task2_response.json()["id"]

    # Add tag to task 1
    client.post(f"/tasks/{task1_id}/tags/{tag_id}", headers=auth_headers)

    # Get tasks by tag
    response = client.get(f"/tasks/by-tag?tag_id={tag_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == task1_id

def test_get_tasks_by_tag_name(client, auth_headers):
    # Create a tag
    tag_data = {"name": "Name Filter Tag"}
    client.post("/tags/", json=tag_data)

    # Create task
    task_data = {
        "title": "Task with Named Tag",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = task_response.json()["id"]

    # Add tag to task
    tag_response = client.get("/tags/")
    tag_id = tag_response.json()[0]["id"]  # Get the first tag
    client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=auth_headers)

    # Get tasks by tag name
    response = client.get("/tasks/by-tag?tag_name=Name%20Filter%20Tag", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == task_id

def test_get_tasks_by_tag_no_params(client, auth_headers):
    response = client.get("/tasks/by-tag", headers=auth_headers)
    assert response.status_code == 400
    assert "Provide either tag_id or tag_name" in response.json()["detail"]