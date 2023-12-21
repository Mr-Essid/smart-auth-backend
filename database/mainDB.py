from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from dbConfig import USERNAME, PASSWORD, HOSTNAME, DATABASE

engine = create_engine(
    f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}",
    echo=True)

print(engine)
