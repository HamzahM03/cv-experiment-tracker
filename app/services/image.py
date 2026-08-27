from sqlalchemy.orm import Session

from app.repositories import dataset as dataset_repo
from app.repositories import image as image_repo
from app.schemas.image import ImageCreate


def create_image(
    db: Session,
    dataset_id: int,
    image_data: ImageCreate,
):
    dataset = dataset_repo.get_dataset_by_id(db, dataset_id)

    if dataset is None:
        return None

    return image_repo.create_image(
        db=db,
        dataset_id=dataset_id,
        filename=image_data.filename,
        file_path=image_data.file_path,
        label=image_data.label,
        split=image_data.split,
        notes=image_data.notes,
    )


def get_images_by_dataset(
    db: Session,
    dataset_id: int,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
):
    dataset = dataset_repo.get_dataset_by_id(db, dataset_id)

    if dataset is None:
        return None

    return image_repo.get_images_by_dataset(
        db=db,
        dataset_id=dataset_id,
        label=label,
        split=split,
        search=search,
        page=page,
        page_size=page_size,
    )


def get_image_count_by_dataset(
    db: Session,
    dataset_id: int,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
):
    return image_repo.get_image_count_by_dataset(
        db=db,
        dataset_id=dataset_id,
        label=label,
        split=split,
        search=search,
    )