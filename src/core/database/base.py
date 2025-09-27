from datetime import datetime

from sqlalchemy import BigInteger, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BigInteger,
        datetime: DateTime(timezone=True),
    }

    metadata = MetaData(
        naming_convention={
            "ix": "ix__%(column_0N_label)s",
            "uq": "uq__%(table_name)s__%(column_0N_name)s",
            "fk": "fk__%(table_name)s__%(column_0N_name)s__%(referred_table_name)s",
            "pk": "pk__%(table_name)s",
        }
    )
