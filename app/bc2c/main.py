from datetime import datetime
from time import time
from anyio import run
from pony.orm import db_session
from pony.orm.core import select
from app.bc2c.binance_client import get_ads
from app.db.models import Cur, BestAd, Ads, Price, Prices  # , Coin, Fee  # for Fees
from app.loader import db


async def cycle(is_first_cycle: bool = False):
    ads = {}
    with db_session:
        if is_first_cycle:
            prev_prices = db.select("select concat(coin, cur, is_sell), array_agg(created_at), array_agg(price) from price where created_at > current_date - interval '30 minutes' and cur = 'RUB' group by (coin, cur, is_sell)")[:]
            prev_prices = {pp[0]: [{"x": int(z[0].timestamp()), "y": z[1]} for z in zip(pp[1], pp[2])] for pp in prev_prices}
            prev_prices = {k: [row for row in sorted(v, key=lambda r: r['x'])] for k, v in prev_prices.items()}
            return prev_prices

        last_price = db.select("select distinct(concat(coin, cur, is_sell)), first_value(price) over (partition by coin, cur, is_sell order by created_at desc) as last_price from price")[:]
        last_price = {lp[0]: lp[1] for lp in last_price}

        ids = select(ba.id for ba in BestAd)[:].to_list()

        # # Get fees info: it's no need to run every cycle
        # fees = select((raw_sql('concat(coin, cur, is_sell)'), f.fee) for f in Fee)[:]
        # fees = {f[0]: f[1] for f in fees}

        for cur in select(c for c in Cur if c.name == 'RUB')[:].to_list():
            pts = list(cur.pts.name)
            for coin in cur.coins.name:
                for isSell in (0, 1):
                    res = await get_ads(coin, cur.name, isSell, pts)
                    ad0 = Ads(res[0]['adv'], pts, 'bc2c').__dict__
                    unq = {k: v for k, v in ad0.items() if k in ['coin', 'cur', 'is_sell', 'ex']}

                    if ad0['id'] in ids:
                        ad0['updated_at'] = datetime.now()
                        BestAd.get(**unq).set(**ad0)
                    else:
                        if ba := BestAd.get(**unq):
                            ba.delete()
                        BestAd(**ad0)

                    key = f"{coin}{cur.name}{('f', 't')[isSell]}"
                    if last_price.get(key) != ad0['price']:
                        p = Prices(res[0]['adv'], pts, 'bc2c')
                        Price(**p.__dict__)

                    ads[key] = [{"x": int(time()), "y": ad0['price']}]  # ad0['id'],

                    # # Get fees info: it's no need to run every cycle
                    # if (f := float(res[0]['adv']['commissionRate'])) != fees.get(key):
                    #     unqf = {'coin': coin, 'cur': cur, 'is_sell': isSell, 'ex': 'bc2c'}
                    #     if fee := Fee.get(**unqf):
                    #         fee.fee = f
                    #     else:
                    #         Fee(**unqf, fee=f)

                    # # need = assets[asset]['target'] - (assets[asset]['free']+assets[asset]['freeze'])

    return ads


if __name__ == "__main__":
    try:
        run(cycle)
    except KeyboardInterrupt:
        print('Stopped.')
