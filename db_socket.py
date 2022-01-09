import asyncpg


class DbSocket:
    def __init__(self):
        self.__connection_pool = None
        self.__connected = False

    async def connect(self):
        self.__connection_pool = await asyncpg.create_pool(
            user='igor',
            password='password',
            database='app',
            host='127.0.0.1',
            port='5432',
        )
        self.__connected = True

    async def execute_query(self, query):
        try:
            if not self.__connected:
                await self.connect()
        except asyncpg.PostgresError:
            # TODO log 'CONNECT ERROR' type(e), e, query
            return None, True

        try:
            async with self.__connection_pool.acquire() as connection:
                result = await connection.fetch(query)
        except asyncpg.PostgresError:
            # TODO log 'EXEC QUERY ERROR' type(e), e, query
            return None, True

        return result, None


db_socket = DbSocket()
