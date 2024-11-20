from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

db_url = "postgresql://admin:1234@db_psql:5437/hostage_emails_db"
engine = create_engine(db_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
def init_db():
    import models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

init_db()
