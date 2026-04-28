import pytest

def test_create_tag(client):
    tag_data = {"name": "Test Tag"}
    response = client.post("/tags/", json=tag_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tag_data["name"]
    assert "id" in data

def test_get_tags(client):
    # Create some tags
    tags_data = [
        {"name": "Tag 1"},
        {"name": "Tag 2"},
        {"name": "Tag 3"}
    ]
    for tag_data in tags_data:
        client.post("/tags/", json=tag_data)

    # Get all tags
    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    tag_names = [tag["name"] for tag in data]
    assert "Tag 1" in tag_names
    assert "Tag 2" in tag_names
    assert "Tag 3" in tag_names