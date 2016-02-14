#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='.', url='mysql+pymysql://stocku:dewgwe54@172.17.0.2/stock', debug='False')
