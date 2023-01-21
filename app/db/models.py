from datetime import datetime
from pony.orm import Required, Set, PrimaryKey, Optional, composite_key, composite_index
from app.loader import db


class Ex(db.Entity):
    name = PrimaryKey(str)
    group = Required(int)
    link = Optional(str)
    ads = Set('Ad')
    prices = Set('Price')
    fees = Set('Fee')
    users = Set('User')


class Cur(db.Entity):
    name = PrimaryKey(str)
    ads = Set('Ad')
    prices = Set('Price')
    pts = Set('Pt')
    fees = Set('Fee')
    coins = Set('Coin')
    users = Set('User')


class Coin(db.Entity):
    name = PrimaryKey(str)
    is_cur = Required(bool, sql_default=False)
    ads = Set('Ad')
    prices = Set('Price')
    fees = Set('Fee')
    curs = Set(Cur)


class Fee(db.Entity):
    cur = Required(Cur)
    coin = Required(Coin)
    ex = Required(Ex)
    is_sell = Required(bool)
    fee = Required(float)
    PrimaryKey(cur, coin, is_sell, ex)


class Pt(db.Entity):
    name = PrimaryKey(str)
    group = Required(int)
    rank = Optional(int, sql_default=1)
    curs = Set(Cur)
    ads = Set('Ad')
    prices = Set('Price')


class User(db.Entity):
    tg_id = Optional(int)
    exs = Set(Ex)
    gmail = Required(str)
    uid = PrimaryKey(int)  # binance id
    no = Optional(str)
    nick = Optional(str)
    cook = Optional(str)
    tok = Optional(str)
    cur = Optional(Cur, sql_default=1)
    ran = Optional(bool, sql_default=False)
    ads = Set('Ad')
    orders = Set('Order')


class Ad(db.Entity):
    id = PrimaryKey(int, size=64)
    coin = Required(Coin)
    cur = Required(Cur)
    is_sell = Required(bool)
    ex = Required(Ex)
    price = Required(float)
    maxFiat = Optional(float)
    minFiat = Optional(float)
    pts = Set(Pt)
    user = Required(User)
    created_at = Required(datetime, precision=0, sql_default='CURRENT_TIMESTAMP')
    updated_at = Required(datetime, precision=0, sql_default='CURRENT_TIMESTAMP')
    composite_key(coin, cur, is_sell, ex)


class Price(db.Entity):
    # id = PrimaryKey(int, auto=True)  # no need, its default behavior
    coin = Required(Coin)
    cur = Required(Cur)
    is_sell = Required(bool)
    ex = Required(Ex)
    price = Required(float)
    pts = Set(Pt)
    created_at = Required(datetime, precision=0, sql_default='CURRENT_TIMESTAMP')
    composite_index(coin, cur, is_sell)


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
#     created_at = Required(datetime, precision=0, sql_default='CURRENT_TIMESTAMP')
#     updated_at = Required(datetime, precision=0, sql_default='CURRENT_TIMESTAMP')
#     composite_key(coin, cur, isSell, ex)  # for only one the best ad existence without history


class Order(db.Entity):
    id = PrimaryKey(int)
    ad: Required(Ad)
    amount: Required(float)
    pt: Required(Pt)
    status: Required(int, sql_default=1)
    user = Required(User)
    created_at = Required(datetime, precision=0, sql_default='CURRENT_TIMESTAMP')


class Prices:
    def __init__(self, adv: {}, banks: [str], ex: str):
        self.is_sell: bool = adv['tradeType'] == 'BUY'  # inverse
        self.coin: str = adv['asset']
        self.cur: str = adv['fiatUnit']
        self.price: float = float(adv['price'])
        self.pts: [Pt] = [pt for pt in banks if pt.name in [a['identifier'] for a in adv['tradeMethods']]]
        self.ex: str = ex


class Ads(Prices):
    def __init__(self, adv: {}, banks: [str], ex: str):
        super().__init__(adv, banks, ex)
        self.id: int = int(adv['advNo']) - 10 ** 19
        self.minFiat: float = float(adv['minSingleTransAmount'])
        self.maxFiat: float = float(adv['dynamicMaxSingleTransAmount'])
        # self.updated_at: datetime = datetime.now()


db.generate_mapping(create_tables=True)
