from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging
from contextlib import asynccontextmanager, contextmanager
from orm.models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """
    Database class to handle connection and session management.
    """

    def __init__(self) -> None:
        """
        Initializes the database connection using credentials from environment variables.
        """
        config = dotenv_values()
        username = config["POSTGRES_USER"]
        password = config["POSTGRES_PASSWORD"]
        host = config["POSTGRES_HOST"]
        db_name = config["POSTGRES_DB"]
        port = 5432
        self.non_async_db_url = (
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
        )
        self.non_asnyc_engine = create_engine(self.non_async_db_url, echo=True)
        self.non_async_session_factory = sessionmaker(
            self.non_asnyc_engine, expire_on_commit=False
        )
        self.db_url = (
            f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"
        )
        self.engine = create_async_engine(self.db_url, echo=True)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_all(self) -> None:
        """
        Create all tables in the database.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        """
        Provide a transactional scope for database operations.
        """
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except Exception as e:
            logger.error(f"Session rollback because of exception: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

    @contextmanager
    def non_async_session(self):
        """
        Provide a transactional scope for database operations.
        """
        session = self.non_async_session_factory()
        try:
            yield session
        except Exception as e:
            logger.error(f"Session rollback because of exception: {e}")
            session.rollback()
            raise
        finally:
            session.close()
