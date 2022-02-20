from sqlalchemy import Column, Integer, Table, String, Float, ForeignKey, MetaData
from sqlalchemy.orm import registry, relationship

from store import model

mapper_registry = registry()
metadata = MetaData()

product_table = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), unique=True, index=True),
    Column("description", String(1000)),
    Column("price", Float),
)

client_table = Table(
    "client",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(100), index=True),
    Column("last_name", String(100), index=True),
)

shopping_order_item_table = Table(
    "shopping_order_item",
    metadata,
    Column("order_id", ForeignKey("shopping_order.id")),
    Column("product_id", ForeignKey("product.id")),
)

shopping_order_table = Table(
    "shopping_order",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("client_id", ForeignKey("client.id")),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Product, product_table)

    mapper_registry.map_imperatively(model.Client, client_table)

    mapper_registry.map_imperatively(
        model.ShoppingOrder,
        shopping_order_table,
        properties={
            "client": relationship(
                model.Client, backref="shopping_orders", order_by=shopping_order_table.c.id
            ),
            "products": relationship(model.Product, secondary=shopping_order_item_table, backref="shopping_orders"),
        },
    )
