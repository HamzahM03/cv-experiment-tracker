from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.services import experiment as experiment_service


router = APIRouter(tags=["experiments"])


@router.post(
    "/projects/{project_id}/experiments",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_experiment(
    project_id: int,
    experiment_data: ExperimentCreate,
    db: Session = Depends(get_db),
):
    experiment = experiment_service.create_experiment(
        db=db,
        project_id=project_id,
        experiment_data=experiment_data,
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Project or dataset not found, or dataset does not belong to project",
        )

    return experiment


@router.get(
    "/experiments/{experiment_id}",
    response_model=ExperimentResponse,
)
def get_experiment(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    experiment = experiment_service.get_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found",
        )

    return experiment

@router.get(
    "/projects/{project_id}/experiments",
    response_model=list[ExperimentResponse],
)
def get_experiments_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    experiments = experiment_service.get_experiments_by_project(
        db=db,
        project_id=project_id,
    )

    if experiments is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return experiments