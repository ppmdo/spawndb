from sqlalchemy.engine import URL

DATABASE_URL = URL(
    drivername='postgresql+psycopg2',
    username='store_app_user',
    password='some_secret',
    host='localhost',
    database='store_app'
)
