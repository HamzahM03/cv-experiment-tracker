from sqlalchemy.orm import Session

from app.repositories import dataset as dataset_repo
from app.repositories import experiment as experiment_repo
from app.repositories import project as project_repo
from app.schemas.experiment import ExperimentCreate


def create_experiment(
    db: Session,
    project_id: int,
    experiment_data: ExperimentCreate,
):
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        return None

    dataset = dataset_repo.get_dataset_by_id(
        db,
        experiment_data.dataset_id,
    )

    if dataset is None:
        return None

    if dataset.project_id != project_id:
        return None

    return experiment_repo.create_experiment(
        db=db,
        project_id=project_id,
        dataset_id=experiment_data.dataset_id,
        name=experiment_data.name,
        model_name=experiment_data.model_name,
        learning_rate=experiment_data.learning_rate,
        epochs=experiment_data.epochs,
        notes=experiment_data.notes,
    )

def get_experiments_by_project(
    db: Session,
    project_id: int,
):
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        return None

    return experiment_repo.get_experiments_by_project(
        db=db,
        project_id=project_id,
    )


def get_experiment_by_id(
    db: Session,
    experiment_id: int,
):
    return experiment_repo.get_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )