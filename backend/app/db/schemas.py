# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from datetime import datetime


class WordSchema(BaseModel):
    words_num: int = Field(..., title="Input words number")
    create_time: datetime = datetime.now()


class WordDB(WordSchema):
    id: int = Field(..., title="Primary key of tb_words")
    create_time: datetime = Field(..., title="Created ar %m/%d/%Y, %H:%M:%S")
    update_time: datetime = None