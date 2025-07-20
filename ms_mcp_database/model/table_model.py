from sqlalchemy import Column, Integer, Date, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    document_name = Column(Text, nullable=False)
    resume_ai = Column(Text, nullable=False)

class Contract(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    document_name = Column(Text, nullable=False)
    resume_ai = Column(Text, nullable=False)