from fastapi import FastAPI
from .route.testdb import router as getdb_router

app = FastAPI()
app.include_router(getdb_router.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to authentication-app!"}

