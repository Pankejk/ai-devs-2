from typing import List, Optional

import uuid

from pydantic import BaseModel, Field

make_uuid = lambda: str(uuid.uuid4())


class PersonModel(BaseModel):
    id: str = Field(default_factory=make_uuid)
    imie: str
    nazwisko: str
    wiek: int
    o_mnie: str
    ulubiona_postac_z_kapitana_bomby: str
    ulubiony_serial: str
    ulubiony_film: str
    ulubiony_kolor: str
    vector: Optional[List[float]] = None
