from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_note_success():
    # create a new note
    payload = {
        "title": "Test Note",
        "content": "This is a test note",
        "done": False
    }

    response = client.post("/notes", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["done"] is False
    assert "created_at" in data


def test_get_notes_list():
    # Get all notes
    response = client.get("/notes")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_note_success():
    # update existing note
    # create note first
    create_resp = client.post(
        "/notes",
        json={"title": "Old", "content": "Old content", "done": False},
    )
    note_id = create_resp.json()["id"]

    update_payload = {
        "title": "Updated title",
        "done": True
    }

    response = client.put(f"/notes/{note_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["done"] is True


def test_delete_note_success():
    # delete note
    create_resp = client.post(
        "/notes",
        json={"title": "Delete me", "content": "Temp", "done": False},
    )
    note_id = create_resp.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204


def test_update_note_not_found():
    # update non-existing note
    response = client.put(
        "/notes/999999",
        json={"title": "Does not exist"},
    )

    assert response.status_code == 404


def test_create_note_validation_error():
    # invalid input
    response = client.post(
        "/notes",
        json={"title": "", "content": ""},
    )

    assert response.status_code == 422
