from sqlalchemy import BigInteger, Column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
