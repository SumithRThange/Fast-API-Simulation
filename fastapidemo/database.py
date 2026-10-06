from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://postgres:7975178423Jio!@localhost:5432/fastapidemo"

engine = create_engine(db_url)


session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
