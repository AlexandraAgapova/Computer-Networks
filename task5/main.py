from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://alexandra:password@pg-db:5432/mydatabase"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class URLRecord(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/parse")
def save_url(url: str = Query(...)):
    session = SessionLocal()
    session.add(URLRecord(url=url))
    session.commit()
    session.close()
    return {"message": f"URL сохранён: {url}"}

@app.get("/urls")
def get_all_urls():
    session = SessionLocal()
    urls = session.query(URLRecord).all()
    session.close()
    return JSONResponse(content=[{"id": u.id, "url": u.url} for u in urls])
