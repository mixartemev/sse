from pony.orm import db_session

from app.db.models import Pt, Cur, Coin, Ex

with db_session:  # curs + pts
    RUB = Cur(name='RUB')
    USD = Cur(name='USD')
    EUR = Cur(name='EUR')
    TRY = Cur(name='TRY')

    Pt(group=0, curs=[USD, EUR, TRY], name='CashInPerson')
    Pt(group=0, curs=[USD, EUR, TRY], name="BANK"),  # blocked in Russia

    Pt(group=4, curs=[RUB, USD, EUR, TRY], name="Advcash"),  # , KZT
    Pt(group=5, curs=[USD, EUR, TRY], name="Payeer"),

    # # # Russia
    Pt(group=1, curs=[RUB], name="TinkoffNew"),
    Pt(group=1, curs=[RUB], name="RosBankNew"),
    Pt(group=1, curs=[RUB], name="PostBankRussia"),
    Pt(group=1, curs=[RUB], name="UralsibBank"),
    Pt(group=1, curs=[RUB], name="RaiffeisenBankRussia"),
    Pt(group=1, curs=[RUB], name="BCSBank"),
    Pt(group=1, curs=[RUB], name="HomeCreditBank"),
    Pt(group=1, curs=[RUB], name="VostochnyBank"),
    Pt(group=1, curs=[RUB], name="RussianStandardBank"),
    Pt(group=1, curs=[RUB], name="ABank"),  # blocked in Russia
    Pt(group=1, curs=[RUB], name="MTSBank"),
    Pt(group=1, curs=[USD, EUR, TRY], name="SpecificBank"),  # blocked in Russia

    Pt(group=2, curs=[RUB], name="YandexMoneyNew"),
    Pt(group=3, curs=[RUB], name="QIWI"),

    Pt(group=6, curs=[RUB], name="RUBfiatbalance"),

    Pt(group=7, curs=[USD, EUR, TRY], name="BanktransferTurkey"),
    Pt(group=7, curs=[USD, EUR, TRY], name="alBaraka"),
    Pt(group=7, curs=[USD, EUR, TRY], name="Akbank"),
    Pt(group=7, curs=[USD, EUR, TRY], name="DenizBank"),
    Pt(group=7, curs=[USD, EUR, TRY], name="Garanti"),
    Pt(group=7, curs=[USD, EUR, TRY], name="HALKBANK"),
    Pt(group=7, curs=[USD, EUR, TRY], name="KuveytTurk"),
    Pt(group=7, curs=[USD, EUR, TRY], name="VakifBank"),
    Pt(group=7, curs=[USD, EUR, TRY], name="Ziraat"),

    Pt(group=8, curs=[USD, EUR, TRY], name="KoronaPay"),  # blocked in Russia

    Coin(name='USDT', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='BTC', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='ETH', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='BNB', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='BUSD', is_cur=True, curs=[RUB, USD, EUR, TRY])
    Coin(name='RUB', is_cur=True, curs=[RUB])
    Ex(name='bc2c', group=5)
