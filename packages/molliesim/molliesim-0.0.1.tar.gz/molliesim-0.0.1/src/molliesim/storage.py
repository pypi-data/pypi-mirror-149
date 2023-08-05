import threading
from collections import defaultdict
from uuid import uuid4

s = threading.BoundedSemaphore(value=1)

MEMSTOR = defaultdict(dict)

PF_PAYMENT = "P"
PF_CUSTOMER = "C"
PF_SUBSCRIPTION = "S"


def clear():
    MEMSTOR.clear()

def set_payment(p):
    with s:
        if not p.id:
            p.id = get_payment_id()
        MEMSTOR[PF_PAYMENT][p.id] = p


def get_payment(pid):
    return MEMSTOR[PF_PAYMENT][p.id]


def get_payment_id():
    while True:
        candidate = f"tr_{str(uuid4()).split('-')[0]}"
        if candidate not in MEMSTOR[PF_PAYMENT]:
            return candidate

    return MEMSTOR[PF_PAYMENT][p.id]


def list_payments():
    return list(MEMSTOR[PF_PAYMENT].values())
