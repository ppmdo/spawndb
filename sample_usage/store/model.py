from typing import *

from dataclasses import dataclass, field


@dataclass
class Product:
    id: int = field(init=False)

    name: str
    description: str
    price: float

    shopping_orders: Optional[List["ShoppingOrder"]] = field(default_factory=list)


@dataclass
class ShoppingOrder:
    id: int = field(init=False)

    client_id: int
    products: List[Product]


@dataclass
class Client:
    id: int = field(init=False)

    first_name: str
    last_name: str
    email: str

    shopping_orders: Optional[List["ShoppingOrder"]] = field(default_factory=list)


