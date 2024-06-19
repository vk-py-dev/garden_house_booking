import hashlib
import json
import secrets

import redis
from fastapi import HTTPException
from starlette.requests import Request

# Establish a connection to your Redis server
r = redis.Redis(host='localhost', port=6379, db=0)


def get_user(username):
    # Use the get method to get the hash associated with the username
    user = r.get(username)
    return user


def generate_token(tokens, username):
    # Generate a random string
    random_string = secrets.token_hex(16)
    # Hash the random string using MD5
    token = hashlib.md5(random_string.encode()).hexdigest()
    # Store the token and user data in Redis
    r.set(token, json.dumps(tokens))
    return token


def get_token(request: Request):
    token = request.cookies.get('token')
    if not token:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return token


def get_user_tokens(token):
    tokens = r.get(token)
    if not tokens:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return json.loads(tokens)
