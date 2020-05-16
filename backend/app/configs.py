# -*- coding: utf-8 -*-
import databases
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()


DATABASE_URL = "mysql://root:123456@192.168.148.129:3306/words"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)

API_PREFIX = "/api/v1.0"

STRFTIME = "%Y-%m-%d %H:%M:%S"
