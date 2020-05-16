# -*- coding: utf-8 -*-
from typing import Tuple
from app.configs import engine, metadata
from sqlalchemy import Table, Column, Integer, TIMESTAMP
from sqlalchemy.sql import func


def timestamps() -> Tuple[Column, Column]:
    return (
        Column("create_time", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
        Column("update_time", TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, onupdate=func.now())

    )

words = Table(
    "words",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("words_num", Integer, nullable=False),
    *timestamps()
)


if __name__ == '__main__':
    metadata.create_all(engine)