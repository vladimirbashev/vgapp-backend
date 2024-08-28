from fastapi import FastAPI

from apps.api.app import api_app

app = FastAPI()

app.mount('/api', api_app)