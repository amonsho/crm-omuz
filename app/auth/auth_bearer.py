from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth_handler import decode_jwt

from db_config import SessionLocal
from sqlalchemy.orm import Session
from app.models import BlackListedToken


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request:Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="invalid authorization code")
        
    def verify_jwt(self, jwtoken: str) ->str:
        try:
            payload = decode_jwt(jwtoken)
            print("decoded payload", payload)
        except Exception as e:
            print('verify_jwt_error', e)
            return False
        
        db:Session = SessionLocal()
        blacklisted = db.query(BlackListedToken).filter(BlackListedToken.token == jwtoken).first()
        db.close()
        if blacklisted:
            return False
        
        return payload is not None