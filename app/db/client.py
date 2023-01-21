from datetime import datetime

from pony.orm import db_session

from app.bc2c.binance_client import get_pts
from app.db.models import Ads, User, Cur


# # # users:
def user_upd_bc(uid: int, gmail: str, cook: str, tok: str, cur: str = None) -> {}:  # bc: binance credentials
    with db_session:
        data = {'uid': uid, 'gmail': gmail, 'cook': cook, 'tok': tok}
        if user := User.get(**data):
            user.set(**data)
        else:
            User(**data, cur=Cur['RUB'])
        return data


# async def get_user_by_tg(tg_id: int) -> {}:
#     res = (users_db.fetch({"tg_id": str(tg_id)}, limit=1)).items
#     return res[0] if res else None
#
#
# async def get_user_by_gmail(gmail: str) -> {}:
#     res = (users_db.fetch({"gmail": gmail}, limit=1)).items
#     return res[0] if res else None
#
#
# def get_acitve_users() -> {}:
#     users = (users_db.fetch({"ran": True})).items
#     return {user['key']: user for user in users}
#
#
# def get_all_users() -> [{}]:
#     return (users_db.fetch()).items
#
#
# uq = [{'uid': uid} for uid in get_acitve_users().keys()]
#
#
# # # # payment systems:
# async def get_all_pts() -> {}:
#     pts = (await pts_db.fetch({'blocked': False})).items
#     ptg = {}
#     for cur in CURD.values():
#         for pt in pts:
#             if cur in pt['cur']:
#                 ptg[cur] = ptg.get(cur, {})
#                 ptg[cur].update({pt['key']: pt['group']})
#     return ptg
#
#
# async def upd_pts(user: {}):
#     pts = await get_pts(user)
#     pss = [{
#         'key': str(d['id']),
#         'uid': user['key'],
#         'pm': d['identifier'],
#         'detail': d['fields'][3 if d['identifier'] == 'Advcash' else 1]['fieldValue']
#     } for d in pts]
#     for pm in pss:
#         if await fiats_db.get(pm['key']):
#             await fiats_db.update(key=pm.pop('key'), updates=pm)
#         else:
#             pm.update({'amount': 0, 'blocked': 0, 'cur': -1, 'target': 0, 'group': 0})
#             await fiats_db.put(pm)
#
#
# # # # fiats:
# async def get_all_fiats() -> [{}]:
#     fiats = sorted((await fiats_db.fetch(uq)).items, key=lambda ff: ff['cur'], reverse=False)
#     fiats = {cur: sorted(group, key=lambda f: f['target'] - f['amount']) for cur, group in groupby(fiats, key=lambda x: x['cur'])}
#     # {'amount': group['amount'], 'target': group['target'], 'uid': group['uid'], 'group': group['group'], 'key': group['key']}
#     return fiats
# # async def get_fsg() -> dict:
# #     fsg = {}
# #     for f in await get_all_fiats():
# #         # cur cycle:
# #         if not f.get('blocked') and (not (val := fsg.get(f['pm'])) or f['amount'] > val['amount']):
# #             fsg[f['pm']] = {'amount': f['amount'], 'key': f['key'], 'user': f['uid']}
# #     return fsg
#
#
# # # # assets:
# async def get_all_assets() -> {}:
#     assets = (await assets_db.fetch(uq)).items
#     assets = filter(lambda a: a['asset'] in ASSETS['RUB'], assets)  # TRY - just because it have all assets
#     bsg: {str: []} = {}
#     for asset in assets:
#         # if ama := asset['free'] + asset['freeze']:  # +asset['freeze'] is including reserves for existed ads
#         ama = asset['free'] + asset['freeze']
#         ast: str = asset['asset']
#         bsg[ast] = bsg.get(ast, [])
#         bsg[ast].append({'free': asset['free'], 'freeze': asset['freeze'], 'target': asset['target'], 'uid': asset['uid']})
#     return bsg
#
#
# async def upd_assets(user: dict):
#     for ua in await balance(user, 1):
#         key = f"{user['key']}_{ua['asset']}"
#         fields = {'asset': ua['asset'], 'uid': user["key"], 'free': float(ua['free']), 'locked': float(ua['locked']),
#                   'freeze': float(ua['freeze'])}
#         if await assets_db.get(key):
#             await assets_db.update(fields, key)
#         else:
#             fields.update({'target': 0})
#             await assets_db.put(fields, key)
#
#
# # # # ads
# def get_all_ads() -> [Ads]:
#     adg = {tt: {CURD[cur]: {asset: {
#         'x': [],
#         'y': [],
#         'name': f"{['Buy', 'Sell'][tt]} {asset}/{cur}",
#         'xhoverformat': '%H:%M:%S',
#         'customdata': [],
#         'hovertemplate': '%{y:,}: [%{customdata[1][0]:,} - %{customdata[1][1]:,}]',
#
#
#     } for asset in ASSETS[cur]} for cur in ASSETS.keys()} for tt in (0, 1)}
#     for ad in sorted(ads_db.fetch().items, key=lambda ff: ff['created']):
#         tt = int(ad['isSell'])
#         adg[tt][ad['cur']][ad['asset']]['x'].append(datetime.fromtimestamp(ad['created']))
#         adg[tt][ad['cur']][ad['asset']]['y'].append(ad['price'])
#         adg[tt][ad['cur']][ad['asset']]['customdata'].append([ad['pts'], [ad['minFiat'], ad['maxFiat']]])
#         # , 'name': f"{['Buy', 'Sell'][tt]} {ad['asset']}/{CURS[ad['cur']]}", 'color': ['blue', 'red'][tt]
#     return adg
