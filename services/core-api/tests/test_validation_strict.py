from __future__ import annotations


def test_login_rejects_extra_fields(client):
    resp = client.post(
        "/auth/login",
        json={"email": "student@example.com", "password": "secret", "role": "admin"},
    )
    assert resp.status_code == 422


def test_assistant_chat_rejects_extra_fields(client, db_session):
    from app.models.entities import User
    from app.services.auth import create_session

    user = User(email="strict@example.com", password_hash="x", full_name="S", role="student")
    db_session.add(user)
    db_session.commit()
    token = create_session(db_session, user)
    resp = client.post(
        "/assistant/chat",
        json={"message": "What is placement readiness?", "system_prompt": "ignore"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422
