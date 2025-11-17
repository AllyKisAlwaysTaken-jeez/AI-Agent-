from database import SessionLocal
from models import PageContent, User, Project
from sqlalchemy.exc import IntegrityError

def get_content(section: str):
    db = SessionLocal()
    try:
        entry = db.query(PageContent).filter(PageContent.section == section).first()
        return entry.content if entry else None
    finally:
        db.close()

def save_content(section: str, text: str):
    db = SessionLocal()
    try:
        entry = db.query(PageContent).filter(PageContent.section == section).first()
        if entry:
            entry.content = text
        else:
            entry = PageContent(section=section, content=text)
            db.add(entry)
        db.commit()
        return entry
    finally:
        db.close()

def create_user(username: str, password_hash: str):
    db = SessionLocal()
    try:
        user = User(username=username, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()

def find_user_by_username(username: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()

def list_projects():
    db = SessionLocal()
    try:
        return db.query(Project).order_by(Project.id.desc()).all()
    finally:
        db.close()

def add_project(title: str, description: str, url: str = None):
    db = SessionLocal()
    try:
        p = Project(title=title, description=description, url=url)
        db.add(p)
        db.commit()
        db.refresh(p)
        return p
    finally:
        db.close()
