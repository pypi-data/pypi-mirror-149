from datetime import date, datetime, time

from bson import ObjectId
from humps.camel import case
from pydantic import BaseModel

from .utils import get_timezone


def to_camel(string):
    return case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.replace(microsecond=0, tzinfo=get_timezone()).isoformat(),
            date: lambda date: date.isoformat(),
            time: lambda time: time.replace(microsecond=0, tzinfo=get_timezone()).isoformat(),
            ObjectId: lambda v: str(v),
        }
        # Needed for the _id to be included when serialised; can't work out how to rename it `id`
        fields = {"id": "_id"}


class FileDownloadRef(CamelModel):
    name: str
    url: str
    extension: str
    size: int
