from fastapi import FastAPI
from routes import users, token

app = FastAPI()
app.include_router(token.router, prefix='/api')
app.include_router(users.router, prefix='/api')
