To launch, enter in the console:
```
uvicorn main:app --reload
```

HTTP request to the local FastAPI server to start parsing:
```
http://127.0.0.1:8000/parse?url=http://books.toscrape.com/catalogue/page-{}.html&limit=10
```

Get all books in JSON format that are saved in PostgreSQL:
```
http://127.0.0.1:8000/books
```
