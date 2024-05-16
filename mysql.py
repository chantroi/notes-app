import os
from typing import Union
from sqlalchemy import create_engine, Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class NoteBase(Base):
    __tablename__ = "notedb"
    name = Column(String, primary_key=True)
    content = Column(String)
    author = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Database:
    def __init__(self) -> None:
        db_url = os.getenv("MYSQL")
        engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add(self, name: str, content: str, author: str = None) -> NoteBase:
        record = NoteBase(name=name, content=content, author=author)
        self.session.add(record)
        self.session.commit()
        return record

    def delete(self, name: str) -> Union[NoteBase | None]:
        record_to_delete = self.session.query(NoteBase).filter_by(name=name).first()
        if record_to_delete:
            self.session.delete(record_to_delete)
            self.session.commit()
            print(f"Deleted book: {record_to_delete.name}")
            return record_to_delete

    def get(self, name: str) -> Union[NoteBase | None]:
        record = self.session.query(NoteBase).filter_by(name=name).first()
        if record:
            return record

    def close(self) -> None:
        self.session.close()
