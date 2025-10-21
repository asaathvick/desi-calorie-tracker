from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Update the DATABASE_URL with your PostgreSQL connection string
DATABASE_URL = "postgresql://user:password@localhost/dc_tracker_db"

engine = create_engine(DATABASE_URL)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit
Base = declarative_base()
