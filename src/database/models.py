from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import declarative_base
from src.database.roles import Role

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)

    # TODO add roles
    role = Column("role", Enum(Role), default=Role.user)
