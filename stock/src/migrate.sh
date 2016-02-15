USER=$MYSQL_ENV_MYSQL_USER_STOCK
HOST=$MYSQL_PORT_3306_TCP_ADDR
PASSWORD=$MYSQL_ENV_MYSQL_PASSWORD_STOCK
DB=$MYSQL_ENV_MYSQL_DATABASE_STOCK
DIR=$(cd $(dirname $0) && pwd)

# https://github.com/openstack/sqlalchemy-migrate/blob/master/migrate/versioning/api.py
python migrate_main.py --user ${USER} --password ${PASSWORD} --host ${HOST} --db ${DB} $@
