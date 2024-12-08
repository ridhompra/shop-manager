from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.database import DatabaseConfig

engine = create_engine(DatabaseConfig.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
