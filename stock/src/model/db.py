import sqlalchemy
from sqlalchemy import Column, TIMESTAMP, Integer, String, Text, Date, Float, ForeignKey,ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    code          = Column('code', Integer, primary_key=True, autoincrement=False)
    name          = Column('stock_name', Text)
    market_code   = Column('market_code', String(1), ForeignKey('market.code'))
    business_code = Column('business_code', Integer, ForeignKey('business.code'))
    create_time   = Column('create_time', TIMESTAMP ,default=sqlalchemy.func.now())
    market        = relationship('Market', backref=backref('market_code', order_by=market_code))
    business      = relationship('Business', backref=backref('business_code', order_by=business_code))

    __table_args__ =    {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    def __init__(self, code,market_code,name,business_code,create_time):
        self.code          = code
        self.name          = name
        self.market_code   = market_code
        self.business_code = business_code
        self.create_time   = create_time
    def __repr__(self):
        return "<Stock('%s','%s', '%s', '%s', '%s')>" % (self.code,self.name,self.market_code, self.name,self.business_code,self.create_time)

class StockDate(Base):
    __tablename__ =  'stock_date'
    stock_code     = Column('stock_code', Integer, ForeignKey('stock.code'), primary_key=True, autoincrement=False)
    date           = Column('date', Date, primary_key=True, autoincrement=False)
    start_price    = Column('start_price', Integer)
    max_price      = Column('max_price', Integer)
    min_price      = Column('min_price', Integer)
    end_price      = Column('end_price', Integer)
    volume         = Column('volume', Integer)
    create_time    = Column('create_time', TIMESTAMP,default=sqlalchemy.func.now())
    stock          = relationship('Stock', backref=backref('stock_code', order_by=stock_code))

    __table_args__ =  {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    def __init__(self, stock_code,date,start_price,max_price,min_price,end_price,volume,create_time):
        self.stock_code  = stock_code
        self.date        = date
        self.start_price = start_price
        self.max_price   = max_price
        self.min_price   = min_price
        self.end_price   = end_price
        self.volume      = volume
        self.create_time = create_time
    def __repr__(self):
        return "<StockDate('%s','%s', '%s', '%s', '%s', '%s', '%s','%s')>" % (self.stock_code,self.date, self.start_price, self.max_price,self.min_price,self.end_price,self.volume,self.create_time)
# 市場
class Market(Base):
    __tablename__ = 'market'
    code        = Column('code', String(1), primary_key=True)
    name        = Column('name', Text)
    create_time = Column('create_time', TIMESTAMP,default=sqlalchemy.func.now())

    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}

    def __init__(self, code, name,create_time):
        self.code = code
        self.name = name
        self.create_time = create_time
    def __repr__(self):
        return "<Stock('%s','%s', '%s')>" % (self.code, self.name,self.create_time)

# 業種
class Business(Base):
    __tablename__ = 'business'
    business_code = Column('code', Integer, primary_key=True, autoincrement=True)
    business_name = Column('name', Text)
    create_time   = Column('create_time', TIMESTAMP,default=sqlalchemy.func.now())

    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}

    def __init__(self, code,name,create_time):
        self.code = code
        self.name = name
        self.create_time   = create_time
    def __repr__(self):
        return "<Business('%s','%s', '%s')>" % (self.code, self.name,self.create_time)

class AnalysisDate(Base):
    __tablename__ = 'analysis_date'
    stock_code   = Column('stock_code', Integer, primary_key=True, autoincrement=False)
    date         = Column('date', Date, primary_key=True, autoincrement=False)
    group_id     = Column('group_id',Integer, ForeignKey('analysis.id'), primary_key=True, autoincrement=False)
    value        = Column('value',Float)

    __table_args__ = (
        ForeignKeyConstraint(['stock_code', 'date'], ['stock_date.stock_code', 'stock_date.date']),
        {'mysql_engine':'InnoDB','mysql_charset':'utf8'}
    )

    def __init__(self, stock_code,date,group_id, value):
        self.stock_code   = stock_code
        self.date         = date
        self.group_id     = group_id
        self.value        = value
    def __repr__(self):
        return "<AnalysisDate('%s', '%s', '%s', '%s')>" % (self.stock_code, self.date, self.group_id, self.value)

class Analysis(Base):
    __tablename__ = 'analysis'
    id            = Column('id',Integer , primary_key=True, autoincrement=True)
    parent_id     = Column('parent_id',Integer, ForeignKey('analysis.id'))
    name          = Column('name',Text)
    display_name  = Column('display_name',Text)

    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}

    def __init__(self, id, parent_id, name, display_name):
        self.id           = id
        self.parent_id    = parent_id
        self.name         = name
        self.display_name = display_name
    def __repr__(self):
        return "<AnalysisGroup('%s', '%s', '%s', '%s')>" % (self.id, self.parent_id, self.name, self.display_name)

class AnalysisParameter(Base):
    __tablename__ = 'analysis_parameter'
    group_id      = Column('group_id',Integer, ForeignKey('analysis.id'), primary_key=True, autoincrement=False)
    key           = Column('key',String(50), primary_key=True)
    value         = Column('value',Text)
    comment       = Column('comment',Text)

    __table_args__ = {'mysql_engine':'InnoDB','mysql_charset':'utf8'}

    def __init__(self, group_id, key, value, comment):
        self.group_id = group_id
        self.key           = key
        self.value         = value
        self.comment       = comment
    def __repr__(self):
        return "<Analysis('%s', '%s', '%s', '%s')>" % (self.group_id, self.key, self.value, self.comment)
