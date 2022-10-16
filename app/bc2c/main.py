from datetime import datetime
from pony.orm import db_session
from pony.orm.core import select

from app.bc2c.binance_client import get_ads
from app.db.models import Cur, Coin, Ad, Ads


async def cycle(first: bool = False):
    ads = {}
    with db_session:
        adsDb = select((a.id, a.coin.name, a.cur.name, a.isSell, a.price) for a in Ad if a.cur.name == 'RUB')
        if first:
            return {a[1]+a[2]+('B', 'S')[int(a[3])]: [a[0] + 10 ** 19, a[4]] for a in adsDb}
        ids = [a[0] for a in adsDb]
        for cur in select(c for c in Cur if c.name == 'RUB')[:].to_list():
            pts = list(cur.pts.name)
            for asset in select(c.name for c in Coin if c.cur):
                res = await get_ads(asset, cur.name, False, pts)
                ad0 = Ads(res[0]['adv'], pts, 'bc2c').__dict__
                unq = {k: v for k, v in ad0.items() if k in ['coin', 'cur', 'isSell', 'ex']}

                if ad0['id'] in ids:
                    ad0['updated_at'] = datetime.now()
                    Ad.get(**unq).set(**ad0)
                else:
                    if ad := Ad.get(**unq):
                        ad.delete()
                    Ad(**ad0)

                ads[asset+cur.name+'B'] = [ad0['id'] + 10 ** 19, ad0['price']]
                # need = assets[asset]['target'] - (assets[asset]['free']+assets[asset]['freeze'])
    return ads


if __name__ == "__main__":
    from anyio import run
    try:
        run(cycle)
    except KeyboardInterrupt:
        print('Stopped.')
