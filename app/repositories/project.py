from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectUpdate


def get_projects(
    db: Session,
    page: int = 1,
    page_size: int = 6,
):
    offset = (page - 1) * page_size

    stmt = (
        select(Project)
        .order_by(Project.id)
        .offset(offset)
        .limit(page_size)
    )

    return db.scalars(stmt).all()

def get_project_count(db: Session):
    stmt = select(func.count()).select_from(Project)
    return db.scalar(stmt)


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
    update_data = project_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project

def delete_project(db: Session, project: Project):
    db.delete(project)
    db.commit()