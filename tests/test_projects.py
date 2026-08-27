from tests.helpers import create_dataset, create_experiment, create_project


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


def test_get_project_detail_renders_project_dataset_and_experiment_info(client, db_session):
    project = create_project(db_session, name="Vision Project", description="desc")
    dataset = create_dataset(db_session, project, name="Street Signs")
    create_experiment(db_session, project, dataset, name="Baseline Run")

    response = client.get(f"/projects/{project.id}/detail")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Vision Project" in response.text
    assert "Street Signs" in response.text
    assert "Baseline Run" in response.text


def test_get_project_detail_not_found_returns_404(client):
    response = client.get("/projects/999999/detail")

    assert response.status_code == 404
