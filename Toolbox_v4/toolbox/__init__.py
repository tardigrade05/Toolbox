from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from toolbox.models import Base

db = create_engine("sqlite:///data.db")
Base.metadata.create_all(db)

print("Hello")
session = Session(db)


