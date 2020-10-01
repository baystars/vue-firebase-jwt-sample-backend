# -*- mode: python -*- -*- coding: utf-8 -*-
from fastapi import (Depends, FastAPI, HTTPException)
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
async def hello():
    return {"text": "hello world!"}

@app.get('/public')
async def hello_public():
    return {"text": "hello public!"}

@app.get('/private')
async def hello_private():
    return {"text": "hello private!"}
