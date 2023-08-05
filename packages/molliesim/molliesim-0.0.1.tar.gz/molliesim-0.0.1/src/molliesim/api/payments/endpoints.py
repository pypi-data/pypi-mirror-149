import re
from http import HTTPStatus


from molliesim.api import parse_body
from molliesim.api.utils import paginate
from molliesim.router import Router
from molliesim import storage

from .models import Payment, PaymentCreate


class PaymentEndpoints:
    CREATE = "/v2/payments/?$"
    READ = "/v2/payments/([^/]+)/?$"
    UPDATE = "/v2/payments/([^/]+)/?$"
    DELETE = "/v2/payments/([^/]+)/?$"
    LIST = "/v2/payments/?$"

    @Router.route("POST", CREATE)
    def create(path, headers, body):
        p = Payment(**parse_body(PaymentCreate, body).dict())
        storage.set_payment(p)
        return p.dict(), HTTPStatus.CREATED

    @Router.route("PUT", UPDATE)
    def update(path, headers, body):
        return {"func": "update", "path": path}, HTTPStatus.OK

    @Router.route("GET", LIST)
    def list(path, headers, body):
        payments = storage.list_payments()
        return paginate("payments", [p.dict() for p in payments]), HTTPStatus.OK

    @Router.route("GET", READ)
    def read(path, headers, body):
        return {"func": "read", "path": path}, HTTPStatus.OK

    @Router.route("DELETE", DELETE)
    def delete(path, headers, body):
        return {"func": "delete", "path": path}, HTTPStatus.OK
