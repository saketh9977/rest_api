from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from datetime import datetime

from helper import get_dish_details
from auth___ import validate_credentials, get_jwt_access_token, validate_jwt_access_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    res = validate_credentials(form_data.username, form_data.password)
    if res == False:
        raise HTTPException(status_code=401, detail="Invalid username-password combo")
    
    jwt_access_token = get_jwt_access_token(form_data.username)    
    return {
        'access_token': jwt_access_token, 
        'token_type': 'bearer'
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    jwt_payload = validate_jwt_access_token(token)
    if jwt_payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return jwt_payload

def get_welcome_message(jwt_payload):
    expiry_timestamp_str = datetime.utcfromtimestamp(jwt_payload['exp']).strftime('%Y-%m-%d %H:%M:%S UTC')
    message = f"hey {jwt_payload['sub']}, your session will expire at {expiry_timestamp_str}"

    return message

@app.get("/")
async def read_items(jwt_payload: dict[str, str] = Depends(get_current_user)):
    expiry_timestamp_str = datetime.utcfromtimestamp(jwt_payload['exp']).strftime('%Y-%m-%d %H:%M:%S UTC')
    message = get_welcome_message(jwt_payload)
    return message

@app.get("/search")
async def read_item(dish, city, jwt_payload: dict[str, str] = Depends(get_current_user)):
    dish_dict = get_dish_details(dish, city)
    message = get_welcome_message(jwt_payload)

    return {
        'message': message,
        'data': dish_dict
    }