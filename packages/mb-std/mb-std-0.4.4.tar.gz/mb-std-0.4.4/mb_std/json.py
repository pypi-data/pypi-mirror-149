import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from json import JSONEncoder

from bson import ObjectId
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult, UpdateResult

from mb_std.mongo import MongoModel


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):

        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, MongoModel):
            return o.dict()
        if isinstance(o, (DeleteResult, UpdateResult)):
            return o.raw_result
        if isinstance(o, InsertOneResult):
            return o.inserted_id
        if isinstance(o, InsertManyResult):
            return o.inserted_ids
        if isinstance(o, ObjectId):
            return str(o)

        return JSONEncoder.default(self, o)


def json_dumps(data) -> str:
    return json.dumps(data, cls=CustomJSONEncoder)
