from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Tenant, User, Project
from sqlalchemy import text

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/set-tenant/{tenant_id}")
def set_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db.execute(text("SET app.current_tenant_id = :tenant_id"), {"tenant_id": tenant_id})
    return {"status": "tenant set", "tenant_id": tenant_id}

@app.get("/projects")
def read_projects(db: Session = Depends(get_db)):
    # RLSが有効ならこのクエリでテナントが絞られる
    result = db.execute(text("SELECT projects.id, projects.name FROM projects JOIN users ON projects.user_id = users.id")).fetchall()
    return [dict(row._mapping) for row in result]