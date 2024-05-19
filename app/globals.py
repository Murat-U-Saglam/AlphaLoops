from db.get_db import Database
from multiprocessing import Queue as MPQueue
from typing import Dict, Callable

global queue
queue = MPQueue()

global task_mapping
task_mapping: Dict[str, Callable[[Dict], str]] = {}

global db
db = Database()
