from sqlalchemy.orm import Session

from app.repositories import project as project_repo
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_projects(db: Session):
    return project_repo.get_projects(db)


def create_project(db: Session, project_data: ProjectCreate):
    return project_repo.create_project(
        db=db,
        name=project_data.name,
        description=project_data.description,
    )

def get_project_by_id(db: Session, project_id: int):
    return project_repo.get_project_by_id(
        db=db,
        project_id=project_id,
    )

def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate,
):
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        return None

    return project_repo.update_project(
        db=db,
        project=project,
        project_data=project_data,
    )

def delete_project(db: Session, project_id: int):
    project = project_repo.get_project_by_id(db, project_id)

    if project is None:
        return False

    project_repo.delete_project(db, project)
    return True