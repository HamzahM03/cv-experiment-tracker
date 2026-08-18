from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services import project as project_service
from app.schemas.project import ProjectCreate, ProjectUpdate
from fastapi import HTTPException
from fastapi import Response, status




router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_projects(db)


@router.post("/")
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    return project_service.create_project(
        db=db,
        project_data=project_data,
    )


@router.get("/{project_id}")
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

@router.patch("/{project_id}")
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