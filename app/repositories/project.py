from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectUpdate


def get_projects(db: Session):
    stmt = select(Project)
    return db.scalars(stmt).all()


def create_project(
    db: Session,
    name: str,
    description: str | None,
):
    project = Project(
        name=name,
        description=description,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project

def get_project_by_id(db: Session, project_id: int):
    return db.get(Project, project_id)


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
):
    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project