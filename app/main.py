from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Tenant, User, Project
from sqlalchemy import text

app = FastAPI()


def get_db():
    db = SessionLocal()
    print(f"New session created: {id(db)}")  # セッションのインスタンスIDをログに出力
    try:
        yield db
    finally:
        db.close()
        print(f"Session closed: {id(db)}")  # セッションが閉じられたことをログに出力


# テナントごとのRLSを有効化するための関数
@app.post("/set-tenant/{tenant_id}")
def set_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db.execute(text("SET app.current_tenant_id = :tenant_id"), {"tenant_id": tenant_id})
    return {"status": "tenant set", "tenant_id": tenant_id}

# プロジェクト情報を取得するエンドポイント
@app.get("/projects")
def read_projects(db: Session = Depends(get_db)):
    # RLSが有効ならこのクエリでテナントが絞られる
    result = db.execute(text("SELECT projects.id, projects.name FROM projects JOIN users ON projects.user_id = users.id")).fetchall()
    return [dict(row._mapping) for row in result]


@app.get("/debug/current-tenant")
def debug_current_tenant(db: Session = Depends(get_db)):
    current_tenant_id = db.execute(text("SHOW app.current_tenant_id")).scalar()
    return {"current_tenant_id": current_tenant_id}