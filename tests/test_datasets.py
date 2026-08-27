from tests.helpers import create_dataset, create_image, create_project


def test_get_dataset_detail_renders_dataset_and_project_info(client, db_session):
    project = create_project(db_session, name="Vision Project")
    dataset = create_dataset(db_session, project, name="Street Signs", description="desc")
    create_image(db_session, dataset, filename="sign_01.jpg", label="stop")

    response = client.get(f"/datasets/{dataset.id}/detail")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Street Signs" in response.text
    assert "Vision Project" in response.text
    assert "sign_01.jpg" in response.text


def test_get_dataset_detail_not_found_returns_404(client):
    response = client.get("/datasets/999999/detail")

    assert response.status_code == 404


def test_dataset_images_pagination_reflects_exact_count_with_filters(client, db_session):
    project = create_project(db_session)
    dataset = create_dataset(db_session, project)

    for i in range(13):
        create_image(db_session, dataset, filename=f"cat_{i:02d}.jpg", label="cat")
    create_image(db_session, dataset, filename="dog_01.jpg", label="dog")

    page_one = client.get(f"/datasets/{dataset.id}/detail", params={"label": "cat"})

    assert page_one.status_code == 200
    assert "cat_00.jpg" in page_one.text
    assert "dog_01.jpg" not in page_one.text
    assert "Next" in page_one.text
    assert "Previous" not in page_one.text
    # the active filter must be carried forward into the Next link
    assert "label=cat" in page_one.text

    page_two = client.get(
        f"/datasets/{dataset.id}/detail",
        params={"label": "cat", "page": 2},
    )

    assert page_two.status_code == 200
    assert "cat_12.jpg" in page_two.text
    assert "Next" not in page_two.text
    assert "Previous" in page_two.text
    assert "label=cat" in page_two.text
