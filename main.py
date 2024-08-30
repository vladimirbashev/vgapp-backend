from fastapi import FastAPI
from routes import users, token, files, google_auth

app = FastAPI()
app.include_router(token.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(files.router, prefix='/api')
app.include_router(google_auth.router, prefix='/api')