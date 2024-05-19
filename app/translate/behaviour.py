from translate.pydantic_models import TranslateRequest
import uuid
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from multiprocessing import Queue, current_process
import time
import globals
from translate.crud import get_translations, write_translation
from typing import Dict, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


def background_task_worker(
    task_queue: Queue, task_mapping: Dict[str, Callable[[Dict], str]]
):
    """
    Worker process that fetches and executes tasks from the queue.
    """
    process_name = current_process().name
    while True:
        task_data = task_queue.get()
        task_id = task_data["task_id"]
        if "translate" in task_mapping:
            result = task_mapping["translate"](task_data["text"], task_data["language"])
            write_translation(task_id, task_data["language"], task_data["text"], result)
            logger.info(
                f"[{process_name}] Task {task_id} completed with result: {result}"
            )
        time.sleep(0.5)


@app.post("/translate/")
async def meta_translate(request: TranslateRequest) -> JSONResponse:
    """
    Endpoint to request translation for a given text.
    """
    task_id = str(uuid.uuid4())
    for language in request.languages:
        globals.queue.put(
            {"task_id": task_id, "text": request.text, "language": language}
        )
    return JSONResponse(
        status_code=200, content={"id": task_id, "status": "In Progress"}
    )


@app.get("/translate/{identifier}")
async def meta_translate_get(identifier: str) -> JSONResponse:
    """
    Endpoint to check the status or get translations of a task.
    """
    translations = await get_translations(identifier)
    if translations:
        return JSONResponse({"translations": [t.__dict__ for t in translations]})
    else:
        return JSONResponse({"status": "In Progress"})
