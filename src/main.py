from fastapi import FastAPI, Depends
from fastapi_swagger import patch_fastapi
from contextlib import asynccontextmanager
from tasks.routes import router as task_router
from account.routes import router as account_router
from account.models import UserModel
from auth.token_auth import get_authenticated_user

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


@app.get("/public")
async def public_root():
    return {"message": "This is a public root"}

@app.get("/private")
async def private_root(user = Depends(get_authenticated_user)):
    print(user)
    return {"message": "This is a private root"}

#----
# -- for basic authentication --
# from auth.basic_auth import get_current_user
# @app.get("/private")
# async def private_root(user: UserModel = Depends(get_current_user)):
#     print(user)
#     return {"message": "This is a private root"}