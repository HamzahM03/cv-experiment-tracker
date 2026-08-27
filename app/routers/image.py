from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.image import ImageCreate, ImageResponse
from app.services import dataset as dataset_service
from app.services import image as image_service
from app.template_config import templates

IMAGE_PAGE_SIZE = 12

router = APIRouter(tags=["images"])


@router.post(
    "/datasets/{dataset_id}/images",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_image(
    dataset_id: int,
    image_data: ImageCreate,
    db: Session = Depends(get_db),
):
    image = image_service.create_image(
        db=db,
        dataset_id=dataset_id,
        image_data=image_data,
    )

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return image


@router.get(
    "/datasets/{dataset_id}/images",
    response_model=list[ImageResponse],
)
def get_images_by_dataset(
    dataset_id: int,
    label: str | None = None,
    split: str | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    db: Session = Depends(get_db),
):
    images = image_service.get_images_by_dataset(
        db=db,
        dataset_id=dataset_id,
        label=label,
        split=split,
        search=search,
        page=page,
        page_size=page_size,
    )

    if images is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found",
        )

    return images


@router.get("/datasets/{dataset_id}/images/grid")
def get_images_grid(
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
        name="partials/dataset_images_grid.html",
        context={
            "dataset": dataset,
            "images": images,
            "label": label,
            "split": split,
            "search": search,
            "page": page,
            "page_size": IMAGE_PAGE_SIZE,
            "image_count": image_count,
        },
    )