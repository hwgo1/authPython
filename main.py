from contextlib import asynccontextmanager
from fastapi import FastAPI
from models import db, User, RefreshToken
from routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    db.create_tables([User, RefreshToken], safe=True)
    yield
    db.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "API Funcionando!"}


app.include_router(auth_router, prefix="/api", tags=["auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
