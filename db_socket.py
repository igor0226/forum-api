import asyncpg
from config import app_config


class DbSocket:
    def __init__(self):
        self.__connection_pool = None
        self.__connected = False

    async def connect(self):
        self.__connection_pool = await asyncpg.create_pool(
            user=app_config['db_settings']['user'],
            password=app_config['db_settings']['password'],
            database=app_config['db_settings']['database'],
            host=app_config['db_settings']['host'],
            port=app_config['db_settings']['port'],
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
