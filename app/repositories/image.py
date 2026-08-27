from sqlalchemy.orm import Session

from app.models.image import Image
from sqlalchemy import select, func


def _build_image_filters(
    dataset_id: int,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
):
    filters = [Image.dataset_id == dataset_id]

    if label:
        filters.append(Image.label == label)

    if split:
        filters.append(Image.split == split)

    if search:
        filters.append(Image.filename.ilike(f"%{search}%"))

    return filters


def create_image(
    db: Session,
    dataset_id: int,
    filename: str,
    file_path: str,
    label: str | None,
    split: str | None,
    notes: str | None,
):
    image = Image(
        dataset_id=dataset_id,
        filename=filename,
        file_path=file_path,
        label=label,
        split=split,
        notes=notes,
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return image


def get_images_by_dataset(
    db: Session,
    dataset_id: int,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
):
    filters = _build_image_filters(dataset_id, label, split, search)

    offset = (page - 1) * page_size

    stmt = (
        select(Image)
        .where(*filters)
        .order_by(Image.id)
        .offset(offset)
        .limit(page_size)
    )

    return db.scalars(stmt).all()


def get_image_count_by_dataset(
    db: Session,
    dataset_id: int,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
):
    filters = _build_image_filters(dataset_id, label, split, search)

    stmt = select(func.count()).select_from(Image).where(*filters)

    return db.scalar(stmt)