import os
import sys
import uuid

from sqlalchemy import Column, Integer, Boolean, String, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

root_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(root_dir, "../nord-security/")

sys.path.insert(0, src_dir)
from local_settings_ai import SQL_ALCHEMY_ENGINE, SQL_ALCHEMY_BASE


class NewsTable(SQL_ALCHEMY_BASE):
    __tablename__ = "news"
    __allow_unmapped__ = True

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    info = Column(String, nullable=False)
    date = Column(String, nullable=False)


def main():
    if not database_exists(SQL_ALCHEMY_ENGINE.url):
        create_database(SQL_ALCHEMY_ENGINE.url)
    session = sessionmaker(bind=SQL_ALCHEMY_ENGINE)()
    SQL_ALCHEMY_BASE.metadata.create_all(SQL_ALCHEMY_ENGINE)
    session.close()


if __name__ == "__main__":
    main()
