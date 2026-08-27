from tests.helpers import create_dataset, create_experiment, create_project


def test_create_experiment_fails_when_dataset_belongs_to_different_project(client, db_session):
    project_a = create_project(db_session, name="Project A")
    project_b = create_project(db_session, name="Project B")
    dataset_b = create_dataset(db_session, project_b, name="Dataset B")

    response = client.post(
        f"/projects/{project_a.id}/experiments",
        json={
            "dataset_id": dataset_b.id,
            "name": "Exp 1",
            "model_name": "resnet50",
            "learning_rate": 0.001,
            "epochs": 10,
        },
    )

    assert response.status_code == 404


def test_create_experiment_succeeds_and_links_project_and_dataset(client, db_session):
    project = create_project(db_session)
    dataset = create_dataset(db_session, project)

    response = client.post(
        f"/projects/{project.id}/experiments",
        json={
            "dataset_id": dataset.id,
            "name": "Exp 1",
            "model_name": "resnet50",
            "learning_rate": 0.001,
            "epochs": 10,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["project_id"] == project.id
    assert body["dataset_id"] == dataset.id


def test_get_experiments_by_project_only_returns_that_projects_experiments(client, db_session):
    project_a = create_project(db_session, name="Project A")
    project_b = create_project(db_session, name="Project B")
    dataset_a = create_dataset(db_session, project_a)
    dataset_b = create_dataset(db_session, project_b)

    create_experiment(db_session, project_a, dataset_a, name="Exp A")
    create_experiment(db_session, project_b, dataset_b, name="Exp B")

    response = client.get(f"/projects/{project_a.id}/experiments")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["name"] == "Exp A"
