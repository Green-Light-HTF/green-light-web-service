from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_CONNECTION = "{}:{}@{}:{}/{}".format("dbroot", "dbroot", "localhost", 3306,
                                           "green_light")


SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://{}".format(MYSQL_CONNECTION)
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/DPMS"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
