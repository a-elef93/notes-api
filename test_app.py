from unittest.mock import MagicMock
import pytest
import app as app_module


@pytest.fixture
def client(monkeypatch):
    fake_redis = MagicMock()
    monkeypatch.setattr(app_module, "cache", fake_redis)
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c, fake_redis


def test_add_note(client):
    c, fake = client
    resp = c.post("/notes", json={"text": "hello"})
    assert resp.status_code == 201
    fake.rpush.assert_called_once_with("notes", "hello")


def test_add_note_without_text(client):
    c, fake = client
    resp = c.post("/notes", json={})
    assert resp.status_code == 400
    fake.rpush.assert_not_called()


def test_list_notes(client):
    c, fake = client
    fake.lrange.return_value = ["a", "b"]
    resp = c.get("/notes")
    assert resp.status_code == 200
    assert resp.get_json() == {"notes": ["a", "b"]}
