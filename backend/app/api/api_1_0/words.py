# -*- coding: utf-8 -*-
from fastapi import APIRouter, Path, HTTPException
from typing import List
from datetime import datetime

from app.db.schemas import WordDB, WordSchema
from app.api.api_1_0 import crud
from app.configs import STRFTIME


router = APIRouter()

@router.post("/word", response_model=WordDB, status_code=201)
async def create_word(payload: WordSchema):
    word_id = await crud.post(payload)

    response_object = {
        "id": word_id,
        "words_num": payload.words_num,
        "create_time": datetime.now().strftime(STRFTIME)
        if not payload.create_time
        else payload.create_time,
    }
    return response_object

@router.get("/word/{id}", response_model=WordDB)
async def get_word(id: int = Path(..., gt=0)):
        word = await crud.get(id)
        if not word:
            raise HTTPException(status_code=404, detail="words_num not found")
        return word

@router.get("/word", response_model=List[WordDB])
async def get_all_words():
    return await crud.get_all()

@router.put("/word/{id}", response_model=WordDB)
async def update_word(payload: WordSchema, id: int = Path(..., gt=0)):
    word = await crud.get(id)
    if not word:
        raise HTTPException(status_code=404, detail="words_num not found")

    word_id = await crud.put(id, payload)

    response_object = {
        "id": word_id,
        "words_num": payload.words_num,
        "create_time": payload.create_time,
    }
    return response_object

@router.delete("/word/{id}")
async def delete_word(id: int = Path(..., gt=0)):
    word = await crud.get(id)
    if not word:
        raise HTTPException(status_code=404, detail="words_num not found")

    await crud.delete(id)
    return word