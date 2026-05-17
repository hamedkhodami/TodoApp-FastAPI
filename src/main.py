from datetime import time

from fastapi import FastAPI, Request
from fastapi_swagger import patch_fastapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from tasks.routes import router as task_router
from account.routes import router as account_router


tags_metadata = [
    {"name": "Tasks",
     "description": "Operations related with tasks",
     "externalDocs": {
         "description": "Task description",
         "url": "/tasks"
     }
     },
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    yield
    print("Application finished")

app = FastAPI(title="Todo Applications",description="this is section for description"
              ,version="0,0,1",terms_of_service="http;//example.com/terms"
              ,contact={
                "name": "Hamed Khodami",
                "email": "khodamihamed77@gmail.com",
               },license_info={"name":"MIT"},lifespan=lifespan, docs_url=None,
              redoc_url=None, swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app)

app.include_router(task_router)
app.include_router(account_router)


# Todo
@app.middleware("http")
async def add_process_time_headers(request: Request, call_next):
    pass

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)