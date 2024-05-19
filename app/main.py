from fastapi import FastAPI
from translate.translator import translate
from translate import route as translate_route
from translate.behaviour import background_task_worker
from contextlib import asynccontextmanager
from multiprocessing import Process
import globals
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await globals.db.create_all()
    globals.task_mapping["translate"] = translate

    # Start the background worker process
    globals.background_process = Process(
        target=background_task_worker, args=(globals.queue, globals.task_mapping)
    )
    globals.background_process.start()
    logger.info("Background process started")

    try:
        yield
    finally:
        logger.info("Shutting down background tasks")
        globals.background_process.terminate()
        globals.background_process.join()
        logger.info("Background process terminated")


app = FastAPI(
    title="Translate API",
    description="Translate API for AlphaLoops",
    version="0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


app.include_router(router=translate_route.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000)
