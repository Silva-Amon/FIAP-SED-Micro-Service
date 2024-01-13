from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from databases import Database

# Database configuration
DATABASE_URL = "mysql+mysqlconnector://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DATABASE']}"
database = Database(DATABASE_URL)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),
    Column("username", String, index=True, nullable=False),
    Column("password", String, nullable=False),
    Column("email", String, nullable=False),
    Column("fullname", String),
)


async def create_table():
    await database.connect()
    await database.execute(users.create())
    await database.disconnect()


async def drop_table():
    await database.connect()
    await database.execute(users.drop())
    await database.disconnect()

