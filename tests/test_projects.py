from tests.helpers import create_project


def test_create_project_persists_and_returns_it(client):
    response = client.post(
        "/projects/",
        json={"name": "CV Model A", "description": "desc"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "CV Model A"
    assert body["description"] == "desc"
    assert "id" in body
    assert "created_at" in body


def test_get_project_not_found_returns_404(client):
    response = client.get("/projects/999999")

    assert response.status_code == 404


def test_update_project_only_changes_provided_fields(client, db_session):
    project = create_project(db_session, name="Original", description="Original desc")

    response = client.patch(
        f"/projects/{project.id}",
        json={"description": "Updated desc"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Original"
    assert body["description"] == "Updated desc"


def test_delete_project_then_get_returns_404(client, db_session):
    project = create_project(db_session)

    delete_response = client.delete(f"/projects/{project.id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/projects/{project.id}")
    assert get_response.status_code == 404
