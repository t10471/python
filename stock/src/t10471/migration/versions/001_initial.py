from sqlalchemy import *
from migrate import *
import sys
import os
ops = os.path.dirname
sd = ops(ops(ops(os.path.abspath(__file__))))
sys.path.append(sd)
from model.db import Stock,StockDate,Market,Business,AnalysisDate,Analysis,AnalysisParameter

def upgrade(migrate_engine):
    Market.__table__.create(migrate_engine)
    Business.__table__.create(migrate_engine)
    Stock.__table__.create(migrate_engine)
    StockDate.__table__.create(migrate_engine)
    Analysis.__table__.create(migrate_engine)
    AnalysisDate.__table__.create(migrate_engine)
    AnalysisParameter.__table__.create(migrate_engine)


def downgrade(migrate_engine):
    migrate_engine.execute('SET FOREIGN_KEY_CHECKS = 0')
    Market.__table__.drop(migrate_engine)
    Business.__table__.drop(migrate_engine)
    Stock.__table__.drop(migrate_engine)
    StockDate.__table__.drop(migrate_engine)
    Analysis.__table__.drop(migrate_engine)
    AnalysisDate.__table__.drop(migrate_engine)
    AnalysisParameter.__table__.drop(migrate_engine)
    migrate_engine.execute('SET FOREIGN_KEY_CHECKS = 1')
