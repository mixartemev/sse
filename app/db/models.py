from datetime import datetime
from pony.orm import Required, Set, PrimaryKey, Optional, composite_key
from app.loader import db


class Ex(db.Entity):
    name = PrimaryKey(str)
    group = Required(int)
    link = Optional(str)
    ads = Set('BestAd')
    prices = Set('Prices')
    fees = Set('Fee')


class Cur(db.Entity):
    name = PrimaryKey(str)
    ads = Set('BestAd')
    prices = Set('Prices')
    pts = Set('Pt')
    fees = Set('Fee')


class Coin(db.Entity):
    name = PrimaryKey(str)
    cur = Required(bool, sql_default=False)
    ads = Set('BestAd')
    prices = Set('Prices')
    fees = Set('Fee')


class Fee(db.Entity):
    cur = Required(Cur)
    coin = Required(Coin)
    ex = Required(Ex)
    isSell = Required(bool)
    fee = Required(float)
    PrimaryKey(cur, coin, isSell, ex)


class Pt(db.Entity):
    name = PrimaryKey(str)
    group = Required(int)
    curs = Set(Cur)
    ads = Set('BestAd')
    prices = Set('Prices')


class BestAd(db.Entity):
    id = PrimaryKey(int, size=64)
    coin = Required(Coin)
    cur = Required(Cur)
    isSell = Required(bool)
    ex = Required(Ex)
    price = Required(float)
    maxFiat = Optional(float)
    minFiat = Optional(float)
    pts = Set(Pt)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    composite_key(coin, cur, isSell, ex)


class Prices(db.Entity):
    adId = PrimaryKey(int, size=64)
    coin = Required(Coin)
    cur = Required(Cur)
    isSell = Required(bool)
    ex = Required(Ex)
    price = Required(float)
    pts = Set(Pt)
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    composite_key(coin, cur, isSell, created_at, ex)


# class MyAd(db.Entity):
#     id = PrimaryKey(int, size=64)
#     coin = Required(Coin)
#     cur = Required(Cur)
#     isSell = Required(bool)
#     ex = Required(Ex)
#     fee = Required(float)
#     price = Required(float)
#     maxFiat = Optional(float)
#     minFiat = Optional(float)
#     pts = Set(Pt)
#     created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
#     updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
#     composite_key(coin, cur, isSell, ex)  # for only one the best ad existence without history


# class Order(db.Entity):
#     id = PrimaryKey(int, size=64)
#     coin = Required(Coin)
#     cur = Required(Cur)
#     isSell = Required(bool)
#     ex = Required(Ex)
#     fee = Required(float)
#     price = Required(float)
#     maxFiat = Optional(float)
#     minFiat = Optional(float)
#     pts = Set(Pt)
#     created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
#     updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
#     composite_key(coin, cur, isSell, ex)  # for only one the best ad existence without history


class Ads:
    def __init__(self, adv: {}, banks: [str], ex: str):
        self.id: int = int(adv['advNo']) - 10 ** 19
        self.isSell: bool = adv['tradeType'] == 'BUY'  # inverse
        self.coin: str = adv['asset']
        self.cur: str = adv['fiatUnit']
        self.price: float = float(adv['price'])
        self.pts: [Pt] = [Pt[tm] for tm in banks if tm in [a['identifier'] for a in adv['tradeMethods']]]
        self.minFiat: float = float(adv['minSingleTransAmount'])
        self.maxFiat: float = float(adv['dynamicMaxSingleTransAmount'])
        self.ex: str = ex
        # self.updated_at: datetime = datetime.now()


db.generate_mapping(create_tables=True)
