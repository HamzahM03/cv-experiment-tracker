from sqlalchemy.orm import Session

from app.models.image import Image
from sqlalchemy import select



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
    stmt = select(Image).where(Image.dataset_id == dataset_id).order_by(Image.id)

    if label:
        stmt = stmt.where(Image.label == label)

    if split:
        stmt = stmt.where(Image.split == split)

    if search:
        stmt = stmt.where(Image.filename.ilike(f"%{search}%"))

    offset = (page - 1) * page_size

    stmt = stmt.offset(offset).limit(page_size)

    return db.scalars(stmt).all()