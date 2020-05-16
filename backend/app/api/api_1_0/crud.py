# -*- coding: utf-8 -*-
from datetime import datetime

from app.db.schemas import WordSchema, WordDB
from app.db.models import words
from app.configs import database, STRFTIME


async def post(payload: WordSchema) -> int:
    query = words.insert().values(
        words_num=payload.words_num,
        create_time=datetime.now().strftime(STRFTIME)
        if not payload.create_time
        else payload.create_time,
    )
    return await database.execute(query=query)

async def get(id: int) -> WordDB:
    query = words.select().where(id == words.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    query = words.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: WordSchema) -> WordDB:
    query = (
        words
        .update()
        .where(id == words.c.id)
        .values(payload)
        .returning(words.c.id)
    )
    return await database.fetch_all(query=query)

async def delete(id: int) -> WordDB:
    query = words.delete().where(id == words.c.id)
    return await database.execute(query=query)

