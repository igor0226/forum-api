from .base import BaseModel


class UserModel(BaseModel):
    async def insert(self, about, email, fullname, nickname):
        query = '''
            INSERT INTO users
            (about, email, fullname, nickname)
            VALUES ('{}', '{}', '{}', '{}')
            RETURNING about, email, fullname, nickname;
        '''.format(about, email, fullname, nickname)

        return await self.db_socket.execute_query(query)

    # get user by nickname or email
    async def get_users(self, nickname='', email=''):
        query = '''
            SELECT about, email, fullname, nickname
            FROM users
            WHERE '''

        if nickname and email:
            query += 'nickname = \'{}\' OR email = \'{}\';'.format(nickname, email)
        elif nickname:
            query += 'nickname = \'{}\';'.format(nickname)
        elif email:
            query += 'email = \'{}\';'.format(email)

        return await self.db_socket.execute_query(query)


user_model = UserModel()
