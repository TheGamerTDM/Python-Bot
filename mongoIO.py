import discord


class mongoIO:

    def __init__(self, bot):
        self.config = bot.config
        self.db = bot.motorClient[self.config.mongo['database']]

    async def addUser(self, member: discord.Member, blacklist: bool = False):
        await self.db.users.insert_one(
            {
                "blacklisted": blacklist,
                "id": member.id,
                "name": member.name
            }
        )

    async def userExists(self, member: discord.Member):
        exists = await self.db.users.find_one({"id": {"$eq": member.id}})
        return exists is not None

    async def blacklistUser(self, member: discord.Member):
        if not await self.userExists(member):
            await self.addUser(member, False)
        else:
            await self.db.users.update_one(
                {"id": member.id},
                {
                    "$set": {
                        "blacklisted": True
                    },
                    "$currentDate": {"lastModified": True}
                }
            )

    async def unblacklistUser(self, member: discord.Member):
        if not await self.userExists(member):
            await self.addUser(member, False)
        else:
            await self.db.users.update_one(
                {"id": member.id},
                {
                    "$set": {
                        "blacklisted": False
                    },
                    "$currentDate": {"lastModified": True}
                }
            )

    async def isBlacklisted(self, member: discord.Member):
        a = await self.db.users.find_one({"id": {"$eq": member.id}})
        if a is None:
            return False
        return a["blacklisted"]

    async def addServer(self, server: discord.Guild, prefix: str = None):
        await self.db.settings.insert_one(
            {
                "id": server.id,
                "prefix": prefix
            }
        )

    async def serverExists(self, server: discord.Guild):
        exists = await self.db.settings.find_one({"id": {"$eq": server.id}})
        return exists is not None

    async def getSetting(self, server: discord.Guild, setting: str):
        a = await self.db.settings.find_one({"id": {"$eq": server.id}})
        if a is None:
            return None
        return a[setting]

    async def setPrefix(self, server: discord.Guild, prefix: str):
        if not await self.serverExists(server):
            await self.addServer(server, prefix)
        else:
            await self.db.settings.update_one(
                {"id": server.id},
                {
                    "$set": {
                        "prefix": prefix
                    },
                    "$currentDate": {"lastModified": True}
                }
            )

    async def wipe(self):
        await self.db.users.delete_many({})
        await self.db.settings.delete_many({})
