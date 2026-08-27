from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.experiment import ExperimentCreate, ExperimentResponse
from app.services import dataset as dataset_service
from app.services import experiment as experiment_service
from app.services import project as project_service
from app.template_config import templates


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


@router.get("/experiments/{experiment_id}/detail")
def get_experiment_detail(
    experiment_id: int,
    request: Request,
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

    project = project_service.get_project_by_id(db=db, project_id=experiment.project_id)
    dataset = dataset_service.get_dataset_by_id(db=db, dataset_id=experiment.dataset_id)

    if project is None or dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Related project or dataset not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="pages/experiment_detail.html",
        context={
            "experiment": experiment,
            "project": project,
            "dataset": dataset,
        },
    )


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