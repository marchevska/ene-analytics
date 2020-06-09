# ENE Analytics app
# Copyright 2020 Olga Marchevska
#
# Flask server and DB connection

import os

from flask import Flask
import sqlalchemy as sa
import yaml


ene_app = Flask(__name__)
app_path = os.path.dirname(os.path.realpath(__file__))
ene_app.config['APPLICATION_DIR'] = app_path

creds = yaml.load(open(f'''{app_path}/creds.yaml'''))

db_user = creds['DB'].get("DB_USER")
db_pass = creds['DB'].get("DB_PASS")
db_name = creds['DB'].get("DB_NAME")
cloud_sql_connection_name = creds['DB'].get("CLOUD_SQL_CONNECTION_NAME")

# Identify if running on GAE or locally and set DB URL respectively
if os.environ.get("GAE_APPLICATION") is not None:
    db_url = f'''mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket=/cloudsql/{cloud_sql_connection_name}'''
else:
    db_host = 'localhost'
    db_url = f'''mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}'''

db = sa.create_engine(
    db_url,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,  # 30 seconds
    pool_recycle=1800,  # 30 minutes
)
