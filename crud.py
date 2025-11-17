from database import SessionLocal
entry = db.query(PageContent).filter(PageContent.section == section).first()
if entry:
entry.content = text
else:
entry = PageContent(section=section, content=text)
db.add(entry)
db.commit()
finally:
db.close()


def create_user(username, password_hash):
db = SessionLocal()
try:
user = User(username=username, password_hash=password_hash)
db.add(user)
db.commit()
return user
except IntegrityError:
db.rollback()
return None
finally:
db.close()


def find_user_by_username(username):
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


def add_project(title, description, url=None):
db = SessionLocal()
try:
p = Project(title=title, description=description, url=url)
db.add(p)
db.commit()
return p
finally:
db.close()
