from datetime import datetime, timedelta
from app.config.database import db

books_col = db["books"]

AUTO_ARCHIVE_DAYS = 30

def auto_archive_old_drafts():
    threshold = datetime.utcnow() - timedelta(days=AUTO_ARCHIVE_DAYS)

    books_col.update_many(
        {
            "status": "DRAFT",
            "last_modified": {"$lt": threshold}
        },
        {
            "$set": {
                "status": "ARCHIVED",
                "is_archived": True
            }
        }
    )
