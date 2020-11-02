from databases import Database


async def connect(query):
    username = "webserver"
    pw = ""
    database = f'mysql://${username}:${pw}@localhost:3306/${}'
    await database.connect()
    await database.execute(query=query)
    await database.disconnect()
