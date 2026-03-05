from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

Base.metadata.schema = 'public'
