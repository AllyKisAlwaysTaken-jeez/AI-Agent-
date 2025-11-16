from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Style, Prompt
from schemas import StyleCreate, PromptCreate

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- CRUD Endpoints ---------- #

@app.post("/styles/")
def create_style(style: StyleCreate, db: Session = Depends(get_db)):
    db_style = Style(name=style.name, description=style.description)
    db.add(db_style)
    db.commit()
    db.refresh(db_style)
    return db_style

@app.get("/styles/")
def list_styles(db: Session = Depends(get_db)):
    return db.query(Style).all()

@app.post("/prompts/")
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    db_prompt = Prompt(text=prompt.text, style_id=prompt.style_id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@app.get("/prompts/")
def list_prompts(db: Session = Depends(get_db)):
    return db.query(Prompt).all()
