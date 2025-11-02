from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABBASE_URL = "sqlite:///crm.db"

engine = create_engine(DATABBASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()