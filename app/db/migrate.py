from pony.orm import db_session

from app.db.models import Pt, Cur, Coin, Ex

with db_session:  # curs + pts
    RUB = Cur(name='RUB')
    USD = Cur(name='USD')
    EUR = Cur(name='EUR')
    TRY = Cur(name='TRY')

    Pt(group=0, curs=[USD, EUR, TRY], name="CashInPerson", rank=0)
    Pt(group=0, curs=[USD, EUR, TRY], name="BANK", rank=1)  # blocked in Russia

    Pt(group=4, curs=[RUB, USD, EUR, TRY], name="Advcash", rank=-2)  # , KZT
    Pt(group=5, curs=[RUB, USD, EUR, TRY], name="Payeer", rank=-3)

    # # # Russia
    Pt(group=1, curs=[RUB], name="TinkoffNew", rank=4)
    Pt(group=1, curs=[RUB], name="RosBankNew", rank=3)
    Pt(group=1, curs=[RUB], name="PostBankRussia", rank=2)
    Pt(group=1, curs=[RUB], name="UralsibBank", rank=2)
    Pt(group=1, curs=[RUB], name="RaiffeisenBankRussia", rank=2)
    Pt(group=1, curs=[RUB], name="BCSBank", rank=2)
    Pt(group=1, curs=[RUB], name="HomeCreditBank", rank=2)
    Pt(group=1, curs=[RUB], name="VostochnyBank", rank=2)
    Pt(group=1, curs=[RUB], name="RussianStandardBank", rank=2)
    Pt(group=1, curs=[RUB], name="ABank", rank=2)  # blocked in Russia
    Pt(group=1, curs=[RUB], name="MTSBank", rank=2)
    Pt(group=1, curs=[USD, EUR, TRY], name="SpecificBank", rank=2)  # blocked in Russia

    Pt(group=2, curs=[RUB], name="YandexMoneyNew", rank=5)
    Pt(group=3, curs=[RUB], name="QIWI", rank=2)

    Pt(group=6, curs=[RUB], name="RUBfiatbalance", rank=-1)

    Pt(group=7, curs=[USD, EUR, TRY], name="BanktransferTurkey", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="alBaraka", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="Akbank", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="DenizBank", rank=4)
    Pt(group=7, curs=[USD, EUR, TRY], name="Garanti", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="HALKBANK", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="KuveytTurk", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="VakifBank", rank=3)
    Pt(group=7, curs=[USD, EUR, TRY], name="Ziraat", rank=3)

    Pt(group=8, curs=[USD, EUR, TRY], name="KoronaPay", rank=2)  # blocked in Russia

    Coin(name='USDT', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='BTC', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='ETH', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='BNB', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='BUSD', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='RUB', is_cur=True, curs=[RUB])
    Ex(name='bc2c', group=5)
