from typing import *

from dataclasses import dataclass


@dataclass
class Product:
    id: int

    name: str
    description: str
    price: float


@dataclass
class Client:
    id: int

    first_name: str
    last_name: str
    email: str


@dataclass
class ShoppingOrder:
    id: int

    client_id: int
    products: List[Product]
