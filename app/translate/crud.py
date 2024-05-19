from orm.models import Translation
from sqlalchemy.future import select
import globals
from typing import List

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_translations(identifier: str) -> List[Translation]:
    """
    Get translations from the database.
    """
    async with globals.db.session() as session:
        async with session.begin():
            result = await session.execute(
                select(Translation).filter_by(task_id=identifier)
            )
            result = result.scalars().all()
            for translation in result:
                translation = translation.__dict__
                translation.pop("_sa_instance_state", None)
                translation.pop("id", None)
            logger.info(f"Fetched translations for task_id {identifier}: {result}")

            return result


def write_translation(
    task_id: str, language: str, text: str, translated_text: str
) -> Translation:
    """
    Write translation to the database.
    """
    with globals.db.non_async_session() as session:
        with session.begin():
            translation = Translation(
                task_id=task_id,
                language=language,
                text=text,
                translated_text=translated_text,
            )
            session.add(translation)
            logger.info(f"Added translation {translation}")
            return translation
