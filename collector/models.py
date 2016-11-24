from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from feeder.settings import DATABASE_URL
from datetime import datetime
from sqlalchemy.dialects import postgresql
from psycopg2.extensions import register_adapter, AsIs, adapt, register_type
from sqlalchemy.dialects.postgresql import UUID
import arrow
import uuid

def adapt_arrow(arrow_date):
    return AsIs("'%s'::timestamptz" % str(arrow_date))


def adapt_dict(some_dict):
    return AsIs("'problem'")


register_adapter(arrow.Arrow, adapt_arrow)
# register_adapter(dict, adapt_dict)

Base = declarative_base()


def db_connect():
    return create_engine(DATABASE_URL, echo=False)


class DBSource(Base):
    __tablename__ = 'sources'
    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    scraped_at = Column(DateTime(timezone=True), default=datetime.utcnow(), nullable=False)
    scraped_url = Column(Unicode(400), nullable=False, unique=True)
    domain = Column(Unicode(100), nullable=False)
    files = Column(postgresql.ARRAY(String))
    file_urls = Column(postgresql.ARRAY(String))
