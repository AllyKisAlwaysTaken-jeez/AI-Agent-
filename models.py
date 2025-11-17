from sqlalchemy import Column, Integer, String, Text
from database import Base


class User(Base):
__tablename__ = "users"
id = Column(Integer, primary_key=True, index=True)
username = Column(String(80), unique=True, index=True, nullable=False)
password_hash = Column(String(256), nullable=False)


class PageContent(Base):
__tablename__ = "page_content"
id = Column(Integer, primary_key=True, index=True)
section = Column(String(80), unique=True, index=True)
content = Column(Text)


class Project(Base):
__tablename__ = "projects"
id = Column(Integer, primary_key=True, index=True)
title = Column(String(150), nullable=False)
description = Column(Text)
url = Column(String(300), nullable=True)
