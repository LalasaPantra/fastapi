from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from . import database as db
from .routers import users, posts, auth, vote
from fastapi.middleware.cors import CORSMiddleware
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to create database and tables on startup."""
    db.create_db_and_tables()
    try:
        yield
    finally:
        pass
    # Cleanup code if needed


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)
# app = FastAPI()
# import ipdb
# ipdb.set_trace()
# @app.on_event("startup")
# def on_startup():
#     db.create_db_and_tables()
# def main():
#     # import ipdb
#     # ipdb.set_trace()
#     # _ = (model.User, model.Post)
#     db.create_db_and_tables()
# if __name__ == "__main__":
#     # uvicorn.run(app, reload=True)
#     main()
