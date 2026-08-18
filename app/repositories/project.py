from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


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