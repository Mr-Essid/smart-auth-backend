from sqlalchemy import create_engine
from dbConfig import USERNAME, PASSWORD, HOSTNAME, DATABASE

engine = create_engine(
    f"postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE}",
    echo=True, pool_pre_ping=True)

print(engine)
