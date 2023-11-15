import uuid
from sqlalchemy import Column, String

from tasks.tasks_3.tasks_4_1.local_settings_ai import SQL_ALCHEMY_BASE


class NewsTable(SQL_ALCHEMY_BASE):
    __tablename__ = "news"
    __allow_unmapped__ = True

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    info = Column(String, nullable=False)
    date = Column(String, nullable=False)
