from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.schemas.dataset import DatasetUpdate

def create_dataset(
    db: Session,
    project_id: int,
    name: str,
    description: str | None,
):
    dataset = Dataset(
        project_id=project_id,
        name=name,
        description=description,
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return dataset


def get_datasets_by_project(db: Session, project_id: int):
    stmt = select(Dataset).where(Dataset.project_id == project_id)
    return db.scalars(stmt).all()


def get_dataset_by_id(db: Session, dataset_id: int):
    return db.get(Dataset, dataset_id)


def update_dataset(
    db: Session,
    dataset: Dataset,
    dataset_data: DatasetUpdate,
):
    update_data = dataset_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(dataset, field, value)

    db.commit()
    db.refresh(dataset)

    return dataset


def delete_dataset(db: Session, dataset: Dataset):
    db.delete(dataset)
    db.commit()





