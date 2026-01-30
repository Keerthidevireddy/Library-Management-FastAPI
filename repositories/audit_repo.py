from app.config.database import db
from datetime import datetime

audit_col = db["book_audit"]

def log_status_change(book_id, prev, new, user):
    audit_col.insert_one({
        "book_id": book_id,
        "previous_status": prev,
        "new_status": new,
        "status_changed_by": user,
        "status_changed_at": datetime.utcnow()
    })
