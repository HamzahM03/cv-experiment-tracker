from datetime import datetime

from pydantic import BaseModel, ConfigDict

class ExperimentCreate(BaseModel):
    dataset_id: int
    name: str
    model_name: str
    learning_rate: float
    epochs: int
    notes: str | None = None


class ExperimentUpdate(BaseModel):
    name: str | None = None
    model_name: str | None = None
    learning_rate: float | None = None
    epochs: int | None = None
    train_accuracy: float | None = None
    validation_accuracy: float | None = None
    notes: str | None = None


class ExperimentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    dataset_id: int
    name: str
    model_name: str
    learning_rate: float
    epochs: int
    train_accuracy: float | None
    validation_accuracy: float | None
    notes: str | None
    created_at: datetime