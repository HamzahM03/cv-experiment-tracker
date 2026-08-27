from tests.helpers import create_dataset, create_image, create_project


def test_get_images_by_dataset_filters_by_label_and_search(client, db_session):
    project = create_project(db_session)
    dataset = create_dataset(db_session, project)

    create_image(db_session, dataset, filename="cat_01.jpg", label="cat")
    create_image(db_session, dataset, filename="dog_01.jpg", label="dog")
    create_image(db_session, dataset, filename="cat_02.jpg", label="cat")

    response = client.get(
        f"/datasets/{dataset.id}/images",
        params={"label": "cat", "search": "01"},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["filename"] == "cat_01.jpg"
