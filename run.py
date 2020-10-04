# -*- mode: python -*- -*- coding: utf-8 -*-
import json
import os
from typing import Optional
import urllib.request

from dotenv import load_dotenv
from fastapi import (Depends, FastAPI, HTTPException)
from fastapi.security import OAuth2PasswordBearer
#import jwt
from jose import jwt
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import (Response, JSONResponse, FileResponse)
from starlette.status import HTTP_401_UNAUTHORIZED

load_dotenv(verbose=True)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

TARGET_AUDIENCE = os.environ.get('TARGET_AUDIENCE', 'target')
CERTIFICATE_URL = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'


app = FastAPI(
    title='FastAPI - Auth example',
    description='FastAPI - Auth example using JWT',
    version='0.0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

"""
def parse_token_jwt(token):
    '''PyJWT version'''
    header = jwt.get_unverified_header(token)
    payload = jwt.decode(token, verify=False)
    return (header, payload)
"""

def parse_token_jwt(token, target_audience=TARGET_AUDIENCE,
                    certificate_url=CERTIFICATE_URL):
    '''jose version'''
    response = urllib.request.urlopen(certificate_url)
    certs = json.loads(response.read())
    #will throw error if not valid
    return jwt.decode(token, certs, algorithms='RS256', audience=target_audience)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    #header, payload = parse_token_jwt(token)
    user = parse_token_jwt(token)
    return user

@app.get('/')
async def hello():
    return {'text': 'hello world!'}

@app.get('/public')
async def hello_public():
    return {'text': 'This is public page. Anyone can see this!'}

@app.get('/private')
async def hello_private(user: dict = Depends(get_current_user)):
    #print(user)
    return JSONResponse({'text': f"This is public page. Only you `{user['user_id']}/{user['email']}` can see this."})
