from sqlalchemy import Column, Integer, String, Text
from database import Base

class PageContent(Base):
    __tablename__ = "page_content"
    id = Column(Integer, primary_key=True, index=True)
    section = Column(String(50), nullable=False)  # 'home', 'about'
    content = Column(Text, nullable=False)
    __table_args__ = {'extend_existing': True}

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
