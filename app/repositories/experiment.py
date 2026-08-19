from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experiment import Experiment


def create_experiment(
    db: Session,
    project_id: int,
    dataset_id: int,
    name: str,
    model_name: str,
    learning_rate: float,
    epochs: int,
    notes: str | None,
):
    experiment = Experiment(
        project_id=project_id,
        dataset_id=dataset_id,
        name=name,
        model_name=model_name,
        learning_rate=learning_rate,
        epochs=epochs,
        notes=notes,
    )

    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    return experiment


def get_experiments_by_project(
    db: Session,
    project_id: int,
):
    stmt = (
        select(Experiment)
        .where(Experiment.project_id == project_id)
        .order_by(Experiment.id)
    )

    return db.scalars(stmt).all()


def get_experiment_by_id(
    db: Session,
    experiment_id: int,
):
    return db.get(Experiment, experiment_id)