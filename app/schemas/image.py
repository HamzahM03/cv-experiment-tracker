from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ImageCreate(BaseModel):
    filename: str
    file_path: str
    label: str | None = None
    split: str | None = None
    notes: str | None = None


class ImageUpdate(BaseModel):
    filename: str | None = None
    file_path: str | None = None
    label: str | None = None
    split: str | None = None
    notes: str | None = None


class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dataset_id: int
    filename: str
    file_path: str
    label: str | None
    split: str | None
    notes: str | None
    created_at: datetime