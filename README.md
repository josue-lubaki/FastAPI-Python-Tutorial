Heroku : https://fastapi-tuto.herokuapp.com/ <br>
Production : http://159.223.152.158/ <br>
Course : https://www.youtube.com/watch?v=0sOvCWFmrtA&t=23834s&ab_channel=freeCodeCamp.org

* Create a virtual environment
```> py -3 -m venv venv ```
* Activate bat environment
```>.\venv\Scripts\activate ```
* Install FastApi
```> pip install fastApi[all] ```
* Install All require dependencies
```> pip install -r requirements.txt ```
* Import fastApi into project
```
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Message": "Hello World"}
```
* Run the fastApi module
```> uvicorn main:app --reload```
* Field Types on Python using [Pydantic](https://pydantic-docs.helpmanual.io/) Library 
```
class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []
 ```
 * Import [Pyscopg](https://www.psycopg.org/docs/usage.html) library form postgres/python 
 ```
    import psycopg2
    from psycopg2.extras import RealDictCursor

    # Connect to an existing database
    conn = psycopg2.connect(host='localhost', database='databaseName', user='postgres', password='password', cursor_factory=RealDictCursor, port=5432)
    
    # Open a cursor to perform database operations
    cursor = conn.cursor()

    # Execute a command: this creates a new table
    cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
 ```

 * Importing database and run it :
 ```
 while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='databaseName', user='postgres', password='password', cursor_factory=RealDictCursor, port=5433)
        cursor = conn.cursor()
        print("Database connection was successfull !")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error : ", error)
        time.sleep(2)
 ```

 * Config ORM using [SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)
 ```
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-adress/hostName>:<port>/<databaseName>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5433/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocator = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
 ```

* Validation email & Expose data you want
```
from pydantic immport EmailStr

# retrieve exactly the field you want to expose
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```
* Hashing Password user with [JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
```
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # if user exists
    new_user = db.query(models.User).filter(
        models.User.email == user.email).first()

    if new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with email: {user.email} already exists")

    # hash the password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

```
* Create a router
```
# in router file (routers/user.py):
from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")

    return user


# in the main.py file:

from .routers import user
app = FastAPI()
app.include_router(user.router)
```

* Create [Token](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) JWT
```
# in the auth.py file:
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # change email of user_credentials to user_credentials.username because, i used OAuth2PasswordRequestForm
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password")

    # create a token for the user, and sharing "id" of user
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
```

```
# in the aouth2.py file :
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# which route protect by bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# create_access_method
def create_access_token(data: dict):
    to_encode = data.copy()

    # time expires
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encode_jwt


# method that veify your token if it's valid
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # get same information of sending since login method
        id = payload = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data
```

```
# in the schemas.py file :
class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# in the Utils.py file :

# method that will be used to verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
```

* Alembic import into project
```
# command :> pip install alembic
# command :> alembic init <directoryName>
# command :> alembic revision -m "message"
# command :> alembic heads
# command :> alembic upgrade head || alembic upgrade +1
# command :> alembic downgrade <revisionCode> || alembic downgrade -1
```
```
# in the ".env.py" file:
from app.models import Base
from app.config import settings

config.set_main_option(
    "sqlalchemy.url", f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}")

target_metadata = Base.metadata
```

* Alembic command [DDL](https://alembic.sqlalchemy.org/en/latest/api/ddl.html)
```
# Example revision
def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=text('NOW()'), nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
```
* Autogenerate Alembic
```
Command :> Alembic revision --autogenerate -m "message"
INFO : Don't need @code< models.Base.metadata.create_all(bind=engine) > in the main.py
```

* export all required dependencies on the text file & install all dependencies
```
Command :> pip freeze > "FileName.txt"
Command :> pip install -r "FileName.txt"
```

* Add [CORS](https://fastapi.tiangolo.com/tutorial/cors/)
```
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

* Deploy Heroku
```
- Heroku Postgres : https://devcenter.heroku.com/articles/heroku-postgresql
Command :> heroku addons:create heroku-postgresql:hobby-dev

Command :> heroku login
Command :> heroku create <AppName>
Command :> heroku git:remote -a <AppName>
Command :> git push heroku main
Command :> heroku logs -t
Command :> heroku ps:restart
```

* Never run "revision" command on prod
```
Command :> heroku run "alembic upgrade head"
```

* Ubuntu Command
```
Command :> sudo apt update && sudo apt upgrade -y
Command :> sudo apt install python3-pip
Command :> sudo pip3 install postgresql postgresql-contrib -y
Command :> psql -U <name1>
Command :> \password <name1>
Command :> cd /etc/postgresql/<version>/main
Command :> systemctl restart postgresql
Command :> adduser <name2>
Command :> usermod -aG sudo <name2>
Command :> set -o allexport; source /home/<name2>/.env; set +o allexport
Command :> gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

* Add [SSL certificate](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)
```
Command :> sudo snap install --classic certbot
Command :> sudo certbot --nginx
```