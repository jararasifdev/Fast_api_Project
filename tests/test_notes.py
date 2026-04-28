import pytest

def test_add_note_to_task(client, auth_headers):
    # Create a task first
    task_data = {
        "title": "Task with Notes",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = task_response.json()["id"]

    # Add a note
    note_data = {"content": "This is a test note"}
    response = client.post(f"/tasks/{task_id}/notes", json=note_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == note_data["content"]
    assert data["task_id"] == task_id
    assert "id" in data

def test_add_note_to_nonexistent_task(client, auth_headers):
    note_data = {"content": "This is a test note"}
    response = client.post("/tasks/999/notes", json=note_data, headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_add_note_unauthorized(client):
    note_data = {"content": "This is a test note"}
    response = client.post("/tasks/1/notes", json=note_data)
    assert response.status_code == 401

def test_get_notes_for_task(client, auth_headers):
    # Create a task first
    task_data = {
        "title": "Task with Multiple Notes",
        "description": "Test Description",
        "status": "todo",
        "priority": "medium",
        "due_date": "2024-12-31"
    }
    task_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = task_response.json()["id"]

    # Add multiple notes
    notes_data = [
        {"content": "Note 1"},
        {"content": "Note 2"},
        {"content": "Note 3"}
    ]
    for note_data in notes_data:
        client.post(f"/tasks/{task_id}/notes", json=note_data, headers=auth_headers)

    # Get notes
    response = client.get(f"/tasks/{task_id}/notes", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    note_contents = [note["content"] for note in data]
    assert "Note 1" in note_contents
    assert "Note 2" in note_contents
    assert "Note 3" in note_contents

def test_get_notes_for_nonexistent_task(client, auth_headers):
    response = client.get("/tasks/999/notes", headers=auth_headers)
    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]

def test_get_notes_unauthorized(client):
    response = client.get("/tasks/1/notes")
    assert response.status_code == 401