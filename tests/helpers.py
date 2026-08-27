from app.models.dataset import Dataset
from app.models.experiment import Experiment
from app.models.image import Image
from app.models.project import Project


def create_project(db_session, name="Test Project", description=None):
    project = Project(name=name, description=description)
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


def create_dataset(db_session, project, name="Test Dataset", description=None):
    dataset = Dataset(project_id=project.id, name=name, description=description)
    db_session.add(dataset)
    db_session.commit()
    db_session.refresh(dataset)
    return dataset


def create_experiment(
    db_session,
    project,
    dataset,
    name="Test Experiment",
    model_name="resnet18",
    learning_rate=0.001,
    epochs=5,
):
    experiment = Experiment(
        project_id=project.id,
        dataset_id=dataset.id,
        name=name,
        model_name=model_name,
        learning_rate=learning_rate,
        epochs=epochs,
    )
    db_session.add(experiment)
    db_session.commit()
    db_session.refresh(experiment)
    return experiment


def create_image(
    db_session,
    dataset,
    filename="image.jpg",
    file_path="/data/image.jpg",
    label=None,
    split=None,
    notes=None,
):
    image = Image(
        dataset_id=dataset.id,
        filename=filename,
        file_path=file_path,
        label=label,
        split=split,
        notes=notes,
    )
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)
    return image
