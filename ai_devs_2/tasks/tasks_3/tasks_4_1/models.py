from typing import List, Optional

import uuid

from pydantic import BaseModel, Field

make_uuid = lambda: str(uuid.uuid4())


class NewsModel(BaseModel):
    id: str = Field(default_factory=make_uuid)
    title: str
    url: str
    info: str
    date: str
    vector: Optional[List[float]] = None
