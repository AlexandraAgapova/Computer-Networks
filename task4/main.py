import time

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuring the database
engine = create_engine("postgresql://alexandra:password@localhost:5432/mydatabase")
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    rating = Column(String)
    url = Column(String)

Base.metadata.create_all(engine)

# FastAPI initialization
app = FastAPI()

# Book Parsing
def parse_books_from_site(base_url: str, page_limit: int = 1):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    books_data = []
    for page in range(1, page_limit + 1):
        url = base_url.format(page)
        driver.get(url)
        time.sleep(2)

        books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        for book in books:
            title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
            price = book.find_element(By.CSS_SELECTOR, "p.price_color").text.strip()
            rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]
            link = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
            books_data.append((title, price, rating, link))

    driver.quit()
    return books_data

# API Endpoint
@app.get("/parse")
def parse_endpoint(url: str = Query(..., description="URL-шаблон с {}"), limit: int = 1):
    books = parse_books_from_site(url, limit)
    db = Session()
    for title, price, rating, link in books:
        db.add(Book(title=title, price=price, rating=rating, url=link))
    db.commit()
    db.close()
    return {"message": f"Готово! Сохранено {len(books)} книг в базу."}

@app.get("/books")
def get_all_books():
    db = Session()
    all_books = db.query(Book).all()
    db.close()
    return JSONResponse(content=[
        {"title": b.title, "price": b.price, "rating": b.rating, "url": b.url}
        for b in all_books
    ])
