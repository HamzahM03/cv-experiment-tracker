from sqlalchemy.orm import Session

from app.repositories import dataset as dataset_repo
from app.repositories import project as project_repo
from app.schemas.dataset import DatasetCreate, DatasetUpdate

def create_dataset(
    db: Session,
    project_id: int,
    dataset_data: DatasetCreate,
):
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        return None

    return dataset_repo.create_dataset(
        db=db,
        project_id=project_id,
        name=dataset_data.name,
        description=dataset_data.description,
    )

def get_datasets_by_project(db: Session, project_id: int):
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        return None

    return dataset_repo.get_datasets_by_project(
        db=db,
        project_id=project_id,
    )


def get_dataset_by_id(db: Session, dataset_id: int):
    return dataset_repo.get_dataset_by_id(db, dataset_id)


def update_dataset(
    db: Session,
    dataset_id: int,
    dataset_data: DatasetUpdate,
):
    dataset = dataset_repo.get_dataset_by_id(db, dataset_id)

    if dataset is None:
        return None

    return dataset_repo.update_dataset(
        db=db,
        dataset=dataset,
        dataset_data=dataset_data,
    )


def delete_dataset(db: Session, dataset_id: int):
    dataset = dataset_repo.get_dataset_by_id(db, dataset_id)

    if dataset is None:
        return False

    dataset_repo.delete_dataset(db, dataset)

    return True

