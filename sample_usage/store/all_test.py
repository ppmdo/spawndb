from database.config import DATABASE_URL
from database.orm import metadata

from spawndb import init_test_db, destroy_test_db

from store.model import Client, Product, ShoppingOrder
from sqlalchemy.orm import sessionmaker
from database.orm import start_mappers


def test_create_client():
    try:
        db_engine = init_test_db(DATABASE_URL, metadata)
        start_mappers()

        Session = sessionmaker(db_engine)

        client = Client(
            'Some',
            'Dude',
            'some_dude@website.com'
        )

        with Session() as session:
            session.add(client)
            session.commit()

            assert client.id is not None
            assert isinstance(client.id, int)

    finally:
        destroy_test_db(DATABASE_URL)


def test_create_shopping_cart():
    try:
        db_engine = init_test_db(DATABASE_URL, metadata)
        start_mappers()

        Session = sessionmaker(db_engine)

        client = Client(
            'Some',
            'Dude',
            'some_dude@website.com'
        )

        product_1 = Product(
            name='Cool CD 1',
            description='Awesome Stuff',
            price=10.50
        )

        product_2 = Product(
            name='Cool CD 2',
            description='Uncool crap',
            price=84.5
        )

        with Session() as session:
            session.add(client)
            session.add(product_1)
            session.add(product_2)

            session.commit()

            assert client.id is not None
            assert product_1.id is not None
            assert product_2.id is not None

            order_1 = ShoppingOrder(
                client_id=client.id,
                products=[product_1, product_2]
            )

            session.add(order_1)
            session.commit()

            assert client.shopping_orders is not None
            assert product_1.shopping_orders is not None

    finally:
        destroy_test_db(DATABASE_URL)
