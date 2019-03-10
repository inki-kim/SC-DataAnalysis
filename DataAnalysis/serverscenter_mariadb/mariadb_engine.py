# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from serverscenter_config import ConfigManager

config = ConfigManager.instance()
client = create_engine('mysql://' + config.get_db_id() + ':' + config.get_db_pw() + '@'
                       + config.get_db_host() + ':' + config.get_db_port() + '/'
                       + config.get_db_name() + '?charset=utf8', convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=client))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db(self):
    self.Base.metadata.create_all(self.client)
