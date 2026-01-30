from app.config.database import db

roles_col = db["roles"]

def create_role(role: dict):
    roles_col.insert_one(role)

def list_roles():
    return list(roles_col.find({}, {"_id": 0}))

def delete_role(name: str):
    roles_col.delete_one({"name": name})
