from fastapi import FastAPI
from apps.api.routes import token, files
from apps.api.routes import users

api_app = FastAPI()

api_app.include_router(token.router)
api_app.include_router(users.router)
api_app.include_router(files.router)