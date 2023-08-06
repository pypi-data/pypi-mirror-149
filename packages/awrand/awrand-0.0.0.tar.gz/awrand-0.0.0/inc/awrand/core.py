from typing import *
import uuid
import time
import base64

__all__ = ['rand_seed', 'make_id_int', 'make_id_bytes', 'make_id_str']

rand_seed = uuid.uuid4().int

def make_id_int() -> int:
    return rand_seed + time.perf_counter_ns()


def make_id_bytes() -> bytes:
    id_int = make_id_int()
    return id_int.to_bytes(id_int.bit_length() // 8 + 1, 'big')


def make_id_str() -> str:
    id_bytes = make_id_bytes()
    return base64.urlsafe_b64encode(id_bytes).decode('ascii')