from app.config.database import users_collection

def find_user_by_username(username: str):
    return users_collection.find_one({"username": username})

def find_user_by_email(email: str):
    return users_collection.find_one({"email": email})

def create_user(user_doc: dict):
    users_collection.insert_one(user_doc)
