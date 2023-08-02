from datetime import datetime, timedelta

from common.database import get_article_collection


def count_published_articles() -> int:
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)
    query = {
        "is_published": True,
        "created_at": {"$gte": yesterday}
    }
    published_articles_count = get_article_collection().count_documents(query)
    return published_articles_count


def count_published_articles_last_5_minutes():
    db = get_article_collection()
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=5)
    count = db.count_documents({"is_published": True, "published_at": {"$gte": five_minutes_ago}})
    return count
