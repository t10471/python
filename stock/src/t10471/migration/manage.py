from migrate.versioning.shell import main
import os

def run(body, user, password, host, db):
    current = os.path.dirname(os.path.abspath(__file__))
    u = 'mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db + '?charset=utf8mb4'
    main(body, repository=current, url=u, debug='False')
