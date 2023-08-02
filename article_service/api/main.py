from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException

from .crud import (create_article, get_article_by_id, get_articles, update_article, delete_article, )
from .models import Article
from .utils.article_utils import count_published_articles
from .utils.daily_report import send_daily_report

app = FastAPI()
scheduler = BackgroundScheduler()


@app.post("/articles/", response_model=Article)
async def create_new_article(article: Article):
    return create_article(article)


@app.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    article = get_article_by_id(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.get("/articles/", response_model=list[Article])
async def get_articles_list(skip: int = 0, limit: int = 10):
    return get_articles(skip, limit)


@app.put("/articles/{article_id}", response_model=Article)
async def update_article_by_id(article_id: str, updated_data: Article):
    article = update_article(article_id, updated_data.dict(exclude_unset=True))
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.delete("/articles/{article_id}")
async def delete_article_by_id(article_id: str):
    article = delete_article(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted successfully"}


@app.put("/articles/{article_id}/publish/", response_model=Article)
async def publish_article(article_id: str):
    article = get_article_by_id(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    article.is_published = True
    updated_article = update_article(article_id, article.dict(exclude_unset=True))
    return updated_article


@app.get("/articles/published/", response_model=list[Article])
async def get_published_articles(skip: int = 0, limit: int = 10):
    published_articles = [article for article in get_articles(skip, limit) if article.is_published]
    return published_articles


@app.get("/articles/author/{author_email}", response_model=list[Article])
async def get_articles_by_author(author_email: str, skip: int = 0, limit: int = 10):
    author_articles = [article for article in get_articles(skip, limit) if article.author_email == author_email]
    return author_articles


@app.delete("/articles/{article_id}/delete/")
async def delete_article_by_author(article_id: str, author_email: str):
    article = get_article_by_id(article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_email != author_email:
        raise HTTPException(status_code=403, detail="Not authorized to delete this article")

    delete_article(article_id)
    return {"message": "Article deleted successfully"}


# @app.on_event("startup")
# async def startup_event():
#     scheduler.add_job(send_daily_report, 'interval', days=1, start_date='2023-08-01 00:00:00',
#                       args=[count_published_articles])
