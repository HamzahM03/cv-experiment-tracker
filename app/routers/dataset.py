from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.dataset import DatasetCreate, DatasetResponse, DatasetUpdate
from app.services import dataset as dataset_service


router = APIRouter(tags=["datasets"])


@router.post(
    "/projects/{project_id}/datasets",
    response_model=DatasetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_dataset(
    project_id: int,
    dataset_data: DatasetCreate,
    db: Session = Depends(get_db),
):
    dataset = dataset_service.create_dataset(
        db=db,
        project_id=project_id,
        dataset_data=dataset_data,
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return dataset


@router.get(
    "/projects/{project_id}/datasets",
    response_model=list[DatasetResponse],
)
def get_datasets_by_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    datasets = dataset_service.get_datasets_by_project(
        db=db,
        project_id=project_id,
    )

    if datasets is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return datasets


@router.get(
    "/datasets/{dataset_id}",
    response_model=DatasetResponse,
)
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    dataset = dataset_service.get_dataset_by_id(
        db=db,
        dataset_id=dataset_id,
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return dataset



@router.patch(
    "/datasets/{dataset_id}",
    response_model=DatasetResponse,
)
def update_dataset(
    dataset_id: int,
    dataset_data: DatasetUpdate,
    db: Session = Depends(get_db),
):
    dataset = dataset_service.update_dataset(
        db=db,
        dataset_id=dataset_id,
        dataset_data=dataset_data,
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return dataset

@router.delete(
    "/datasets/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    deleted = dataset_service.delete_dataset(
        db=db,
        dataset_id=dataset_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)