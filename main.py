from fastapi import FastAPI

app = FastAPI()
app.include_router(token.router, prefix='/api')
app.include_router(users.router, prefix='/api')
