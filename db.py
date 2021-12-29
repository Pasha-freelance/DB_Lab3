from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = 'postgresql+psycopg2://postgres:pushokcharlik@localhost/store'
Orders = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
