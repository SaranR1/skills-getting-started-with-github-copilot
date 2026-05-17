from urllib.parse import quote


def test_get_activities(client):
    # Arrange
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "student.new@mergington.edu"

    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert resp.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "dup@test.edu"

    # Act
    resp1 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    resp2 = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert resp1.status_code == 200
    assert resp2.status_code == 400


def test_remove_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "remove@test.edu"
    client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")

    # Assert
    assert resp.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants


def test_remove_nonexistent_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@test.edu"

    # Act
    resp = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")

    # Assert
    assert resp.status_code == 400
