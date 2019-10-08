import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_wtf import CSRFProtect
from  flask_restful import Api
from flask_migrate import Migrate



pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "123456"

BASE_DIR = os.path.join(os.path.dirname(__file__))

# app.config.from_pyfile("settings.py")
app.config.from_object("settings.Config")

import datetime

# ORM关联应用
models = SQLAlchemy(app)
csrf=CSRFProtect(app)

api=Api(app)

migrate=Migrate(app,models) #安装数据库管理插件