from anyio import run


async def actual():
    for user in get_acitve_users().values():
        await upd_pts(user)
        await upd_assets(user)

if __name__ == "__main__":
    try:
        run(actual)
    except KeyboardInterrupt:
        print('Stopped.')