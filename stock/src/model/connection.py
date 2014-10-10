#*- coding: utf-8 -*-

import sqlalchemy
import sqlalchemy.orm
import config

class dbManager(object):
    def __init__(self, user, password, db, host):
        #engine = sqlalchemy.create_engine('mysql://eccube:eccube@localhost/stock', echo=True)
        engine = sqlalchemy.create_engine('mysql://'+ user + ':' + password + '@' + host + '/' + db)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.sess = Session()

    def getSession(self):
        return self.sess
#sqlalchemy.orm.mapper(Daily_stock,daily_stock)

manager = dbManager(user = config.DB_USER, password = config.DB_PASSWORD, db = config.DB_DB, host = config.DB_HOST)

def get_session():
    return manager.getSession()