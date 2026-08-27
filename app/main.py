from fastapi import FastAPI, Request
from app.routers.projects import router as projects_router
from app.routers.dataset import router as dataset_router
from app.routers.image import router as image_router
from app.routers.experiments import router as experiments_router
from app.template_config import templates





app = FastAPI()


app.include_router(projects_router)
app.include_router(dataset_router)
app.include_router(image_router)
app.include_router(experiments_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )