from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt

"""
    warning: store user data in more secure place, not in code.
    this is for testing only, not to be used on prod
"""
USER_DATA = {
    'john': {
        'hashed_password': '$2b$12$H2qyP7Yk4KHLvxH6wpIla.KX/OCpJiqGAOHTnBs51iNjq1hE0Ld3.'
    }
}

"""
    warning: do not store Symmetric keys in code. This is for testing only.
"""
# Use 'openssl rand -hex 32' to generate 32 bytes of random hex chars
JWT_SYMMETRIC_KEY = '696b346ef005ead8016222499d0661acc34225be0254ed6a6192068119cab1f5'
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRY_MINUTES = 3

bcrypt_ = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_credentials(username, plain_password):
    if (username in USER_DATA) == False:
        return False
    
    res = bcrypt_.verify(plain_password, USER_DATA[username]['hashed_password'])
    if not res:
        return False
    
    return True

def get_jwt_access_token(username):
    jwt_payload = {
        'sub': username,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_TOKEN_EXPIRY_MINUTES)
    }
    jwt_access_token = jwt.encode(jwt_payload, JWT_SYMMETRIC_KEY, algorithm=JWT_ALGORITHM)

    return jwt_access_token

def validate_jwt_access_token(jwt_access_token):
    
    jwt_payload = None
    try:
        jwt_payload = jwt.decode(jwt_access_token, JWT_SYMMETRIC_KEY, algorithms=[JWT_ALGORITHM])
    except:
        return None
    
    username = jwt_payload.get("sub")
    if username is None:
        return None
    
    if (username in USER_DATA) == False:
        return None
    
    return {
        'sub': jwt_payload['sub'],
        'exp': jwt_payload['exp']
    }