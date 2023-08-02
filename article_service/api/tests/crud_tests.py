from fastapi.testclient import TestClient

from article_service.api.main import app

client = TestClient(app)
article_data = {"title": "Test Article",
                "content": "This is a test article content.",
                "author_email": "test@example.com"}


def test_create_new_article():
    response = client.post("/articles/", json=article_data)
    assert response.status_code == 200
    article = response.json()
    assert article["title"] == "Test Article"
    assert article["content"] == "This is a test article content."
    assert article["author_email"] == "test@example.com"
    assert not article["is_published"]


def test_get_article():
    article_id = client.post("/articles/", json=article_data).json().get('id')
    response = client.get(f"/articles/{article_id}")
    assert response.status_code == 200
    article = response.json()
    assert article["title"] == "Test Article"
    assert article["content"] == "This is a test article content."
    assert article["author_email"] == "test@example.com"
    assert not article["is_published"]


def test_get_articles_list():
    client.post("/articles/", json=article_data)
    response = client.get("/articles/")
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 1


def test_get_empty_articles_list():
    response = client.get("/articles/")
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 0


def test_update_article_by_id():
    article_id = client.post("/articles/", json=article_data).json().get('id')
    updated_data = article_data
    updated_data['title'] = 'New title'
    response = client.put(f"/articles/{article_id}", json=updated_data)
    assert response.status_code == 200
    article = response.json()
    assert article["title"] == 'New title'


def test_delete_article_by_id():
    article_id = client.post("/articles/", json=article_data).json().get('id')
    response = client.delete(f"/articles/{article_id}")
    assert response.status_code == 200
    message = response.json()
    assert message["message"] == "Article deleted successfully"


def test_publish_article():
    article_id = client.post("/articles/", json=article_data).json().get('id')
    response = client.put(f"/articles/{article_id}/publish/")
    assert response.status_code == 200
    article = response.json()
    assert article["is_published"]


def test_get_published_articles():
    article_id = client.post("/articles/", json=article_data).json().get('id')
    client.put(f"/articles/{article_id}/publish/")
    response = client.get("/articles/published/")
    assert response.status_code == 200
    articles = response.json()
    for article in articles:
        assert article["is_published"]


def test_get_articles_by_author():
    client.post("/articles/", json=article_data).json().get('id')
    response = client.get("/articles/author/test@example.com")
    assert response.status_code == 200
    articles = response.json()
    for article in articles:
        assert article["author_email"] == "test@example.com"


def test_delete_article_by_author():
    article_id = client.post("/articles/", json=article_data).json().get('id')
    response = client.delete(f"/articles/{article_id}/delete/?author_email=test@example.com")
    assert response.status_code == 200
    message = response.json()
    assert message["message"] == "Article deleted successfully"
