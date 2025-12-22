from sqlalchemy import Column, String, Integer, Boolean, Date
import datetime as dt
from database.session import Base

class User (Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String, unique=True)
    password_hash = Column("password", String)
    is_activate = Column("activate", Boolean, default=True)
    is_admin = Column("admin", Boolean, default=False)
    create_at = Column("create_at", Date, default=lambda: dt.date.today())