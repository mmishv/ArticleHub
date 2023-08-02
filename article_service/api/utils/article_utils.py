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
