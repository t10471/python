import sqlalchemy
import sqlalchemy.orm
import t10471.model.config as config

class dbManager():

    def __init__(self, user, password, host, db):
        u = 'mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db + '?charset=utf8mb4'
        engine = sqlalchemy.create_engine(u)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.sess = Session()

    def getSession(self):
        return self.sess

manager = dbManager(user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST, db=config.DB_DB)

def get_session():
    return manager.getSession()
