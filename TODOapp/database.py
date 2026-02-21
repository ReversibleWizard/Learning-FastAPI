from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://deployed_todo_db_user:HxXC81a43UqdrWJtY5mNOatq3iq7olwg@dpg-d6cqh8ngi27c7386i620-a/deployed_todo_db'  # also have to install psycopg2-binary
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:sayak2004@127.0.0.1:3306/todoapplicationdatabase' # also need to install pymysql package to use mysql
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
