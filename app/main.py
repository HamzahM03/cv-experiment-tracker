from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.routers.projects import router as projects_router
from app.routers.dataset import router as dataset_router



app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


app.include_router(projects_router)
app.include_router(dataset_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
    )