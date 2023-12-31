from bson import ObjectId
from typing import List, Optional
from datetime import datetime

from common.database import get_article_collection
from common.rabbitmq import channel
from .models import Article


def create_article(article: Article) -> Article:
    article_data = {
        "title": article.title,
        "content": article.content,
        "author_email": article.author_email,
        "created_at": datetime.utcnow(),
        "is_published": article.is_published,
    }
    get_article_collection().insert_one(article_data)
    return article


def get_article_by_id(article_id: str) -> Optional[Article]:
    article_data = get_article_collection().find_one({"_id": ObjectId(article_id)})
    if article_data:
        article = Article(**article_data)
        return article
    else:
        return None


def get_articles(skip: int = 0, limit: int = 10) -> List[Article]:
    articles_data = get_article_collection().find().skip(skip).limit(limit)
    articles = [Article(**article_data) for article_data in articles_data]
    return articles


def update_article(article_id: str, updated_data: dict) -> Optional[Article]:
    result = get_article_collection().update_one(
        {"_id": ObjectId(article_id)}, {"$set": updated_data}
    )
    if result.modified_count == 1:
        updated_article = get_article_by_id(article_id)
        return updated_article
    else:
        return None


def delete_article(article_id: str) -> bool:
    result = get_article_collection().delete_one({"_id": ObjectId(article_id)})
    return result.deleted_count == 1
