from flask_sqlalchemy import SQLAlchemy
import pymysql

# python3.*报“ImportError: No module named ‘MySQLdb'”
pymysql.install_as_MySQLdb()
db = SQLAlchemy()
