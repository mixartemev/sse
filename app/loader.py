from deta import Deta
from pony.orm import Database, set_sql_debug

db = Database()
set_sql_debug(True)
db.bind(provider='postgres', user='artemiev', password='', host='localhost', database='arbitrage')

deta = Deta('c05c0tj9_w5FFYcKFyUiCr5X9c3sBK29hitinzzQD')
users_db = deta.Base("users")
fiats_db = deta.Base("fiats")
pts_db = deta.Base("pts")
assets_db = deta.Base("assets")
ads_db = deta.Base('ads')
orders_db = deta.Base('orders')

def_user = users_db.get('357058112')
