from fastapi import APIRouter, Depends, HTTPException, Query, Request, status, Response
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.dataset import DatasetCreate, DatasetResponse, DatasetUpdate
from app.services import dataset as dataset_service
from app.services import image as image_service
from app.services import project as project_service
from app.template_config import templates

IMAGE_PAGE_SIZE = 12

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


@router.get("/datasets/{dataset_id}/detail")
def get_dataset_detail(
    dataset_id: int,
    request: Request,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    dataset = dataset_service.get_dataset_by_id(db=db, dataset_id=dataset_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    project = project_service.get_project_by_id(db=db, project_id=dataset.project_id)

    images = image_service.get_images_by_dataset(
        db=db,
        dataset_id=dataset_id,
        label=label,
        split=split,
        search=search,
        page=page,
        page_size=IMAGE_PAGE_SIZE,
    )

    image_count = image_service.get_image_count_by_dataset(
        db=db,
        dataset_id=dataset_id,
        label=label,
        split=split,
        search=search,
    )

    return templates.TemplateResponse(
        request=request,
        name="pages/dataset_detail.html",
        context={
            "dataset": dataset,
            "project": project,
            "images": images,
            "label": label,
            "split": split,
            "search": search,
            "page": page,
            "page_size": IMAGE_PAGE_SIZE,
            "image_count": image_count,
        },
    )


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