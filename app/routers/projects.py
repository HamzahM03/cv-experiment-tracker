from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.services import project as project_service
from app.schemas.project import ProjectCreate



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