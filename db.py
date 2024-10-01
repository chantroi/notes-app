import os
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
Base = declarative_base()


class Note(Base):
    __tablename__ = "notes"

    name = Column(String, primary_key=True)
    content = Column(String)

    def __repr__(self):
        return f"Note({self.name}, {self.content})"


class DB:
    def __init__(self):
        engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        self.session = SessionLocal()

    def add(self, name: str, content: str) -> None:
        note = Note(name=name, content=content)
        self.session.merge(note)
        self.session.commit()

    def delete(self, name: str) -> None:
        note = self.get(name)
        self.session.delete(note)
        self.session.commit()

    def get(self, name: str) -> Note:
        return self.session.query(Note).filter_by(name=name).first()
