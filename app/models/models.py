

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean


metadata = MetaData()


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_admin", Boolean),
    Column("is_developer", Boolean),
    Column("is_user", Boolean),
)
