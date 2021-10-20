import asyncpg


class DbSocket:
    def __init__(self):
        self.__db_socket = None

    async def connect(self):
        self.__db_socket = await asyncpg.connect(
            user='igor',
            password='password',
            database='app',
            host='127.0.0.1',
            port='5432',
        )

    async def close(self):
        await self.__db_socket.close()

    async def execute_query(self, query):
        try:
            await self.connect()
        except asyncpg.PostgresError:
            # TODO log 'CONNECT ERROR' type(e), e, query
            return None, True

        try:
            result = await self.__db_socket.fetch(query)
        except asyncpg.PostgresError:
            # TODO log 'EXEC QUERY ERROR' type(e), e, query
            return None, True

        try:
            await self.close()
        except asyncpg.PostgresError:
            # TODO log 'CLOSE ERROR' type(e), e, query
            return None, True

        return result, None


db_socket = DbSocket()
