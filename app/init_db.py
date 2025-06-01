from db import SessionLocal
from models import Tenant, User, Project

db = SessionLocal()

# 既存データ削除（開発用途）
db.query(Project).delete()
db.query(User).delete()
db.query(Tenant).delete()

# テナント作成
tenant1 = Tenant(name="Company A")
tenant2 = Tenant(name="Company B")
db.add_all([tenant1, tenant2])
db.commit()

# ユーザー作成
user1 = User(name="Alice", tenant_id=tenant1.id)
user2 = User(name="Bob", tenant_id=tenant2.id)
db.add_all([user1, user2])
db.commit()

# プロジェクト作成
project1 = Project(name="Project A", user_id=user1.id)
project2 = Project(name="Project B", user_id=user2.id)
db.add_all([project1, project2])
db.commit()

print("データベース初期化完了")
db.close()
