from http import HTTPStatus
from pydantic import BaseModel, ValidationError, validator


class ParseException(Exception):
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)


def parse_body(schema_cls, body):
    try:
        p = schema_cls(**body)
        return p
    except ValidationError as err:
        for err in err.errors():
            raise ParseException({
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
                "title": "Unprocessable Entity",
                "detail": err["msg"],
                "field": ".".join(err["loc"]),
            })
        raise
