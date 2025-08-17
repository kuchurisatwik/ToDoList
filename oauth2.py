import routers.auth as auth,DataBase,schemas,models

from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')


SECRET_KEY = 'DFLKJDSKLFJESDSNK3JKJR8IJ38URIOEH9WHER983U9E984Y'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 180

def create_access_token(data:dict):
    to_encode = data.copy()

    expire_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire_time})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)

    return encode_jwt


def decode_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # don't force-annotate here; read and validate:
        user_id = payload.get("user_id")
        # ensure it's present
        if user_id is None:
            raise credentials_exception

        # try to coerce to int safely in case it came as a string
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception

        # create TokenData that has user_id attribute
        token_data = schemas.TokenData(user_id=user_id)
        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(DataBase.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}   # correct header name
    )

    token_data = decode_access_token(token, credentials_exception)

    # token_data.user_id exists because we set it above
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user

"""focus on type conversions and type castings, and remember that this kind of errors are commonly 
repetative and focus on line to line implementation to get better grasp at variable reassigings..."""
# def decode_access_token(token:str,credentials_exception):
#     try:
#         payload = jwt.decode(token,SECRET_KEY, algorithms = [ALGORITHM])
#         user_id:int = payload.get("user_id")
#         print(user_id)

#         if user_id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id = id)
#         return token_data
    
#     except JWTError:
#         raise credentials_exception
    
    
#     # payload = jwt.decode(token,SECRET_KEY, algorithms = [ALGORITHM])
#     # user_id:str = payload.get("user_id")
#     # print(user_id)

#     # if user_id is None:
#     #     raise credentials_exception
#     # token_data = schemas.TokenData(id = str(user_id))
#     # return token_data


# def get_current_user(token: str = Depends(oauth2_scheme),
#                      db:Session = Depends(DataBase.get_db)):
#     credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
#                                           detail = f"Could not validate credentials",
#                                           headers = {"WWW-Authentication":"Bearer"})
#     token = decode_access_token(token, credentials_exception)

#     user = db.query(models.User).filter(models.User.id == token.user_id).first()
#     return user
