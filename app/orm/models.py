from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Translation(Base):
    __tablename__ = "translations"
    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    text = Column(String)
    language = Column(String)
    translated_text = Column(String)

    def __repr__(self) -> str:
        return f"Translation(task_id={self.task_id}, text={self.text}, language={self.language})"
