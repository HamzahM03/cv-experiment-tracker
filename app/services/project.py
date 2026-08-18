from sqlalchemy.orm import Session

from app.repositories import project as project_repo
from app.schemas.project import ProjectCreate


def get_projects(db: Session):
    return project_repo.get_projects(db)


def create_project(db: Session, project_data: ProjectCreate):
    return project_repo.create_project(
        db=db,
        name=project_data.name,
        description=project_data.description,
    )