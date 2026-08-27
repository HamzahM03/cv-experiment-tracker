from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, Query

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services import project as project_service
from app.services import dataset as dataset_service
from app.services import experiment as experiment_service
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.template_config import templates


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def get_projects(request:Request, page:int = Query(default=1, ge=1), db: Session = Depends(get_db)):
    projects = project_service.get_projects(db, page=page, page_size=6)

    PAGE_SIZE = 6

    total_count = project_service.get_project_count(db)


    return templates.TemplateResponse(
    request=request,
    name="pages/projects.html",
    context={
        "projects": projects,
        "page":page,
        "page_size": PAGE_SIZE,
        "total_count": total_count,
        },
    )

@router.get("/grid")
def get_projects_grid(
    request: Request,
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    page_size = 6

    projects = project_service.get_projects(
        db=db,
        page=page,
        page_size=page_size,
    )

    total_count = project_service.get_project_count(db)

    return templates.TemplateResponse(
        request=request,
        name="partials/projects_grid.html",
        context={
            "projects": projects,
            "page": page,
            "page_size": page_size,
            "total_count": total_count,
        },
    )


@router.post("/", response_model=ProjectResponse, status_code = 201)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    return project_service.create_project(
        db=db,
        project_data=project_data,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = project_service.get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project


@router.get("/{project_id}/detail")
def get_project_detail(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    project = project_service.get_project_by_id(
        db=db,
        project_id=project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    datasets = dataset_service.get_datasets_by_project(db=db, project_id=project_id)
    experiments = experiment_service.get_experiments_by_project(db=db, project_id=project_id)
    dataset_by_id = {dataset.id: dataset for dataset in datasets}

    return templates.TemplateResponse(
        request=request,
        name="pages/project_detail.html",
        context={
            "project": project,
            "datasets": datasets,
            "experiments": experiments,
            "dataset_by_id": dataset_by_id,
        },
    )

@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = project_service.update_project(
        db=db,
        project_id=project_id,
        project_data=project_data,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    deleted = project_service.delete_project(
        db=db,
        project_id=project_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)