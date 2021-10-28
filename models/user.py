from .base import BaseModel


class UserModel(BaseModel):
    def create_user(self, about, email, fullname, nickname):
        query = '''
            INSERT INTO users
            (about, email, fullname, nickname)
            VALUES ('{}', '{}', '{}', '{}')
            RETURNING about, email, fullname, nickname;
        '''.format(about, email, fullname, nickname)

        return self.db_socket.execute_query(query)

    # get user by nickname or email
    def get_users(self, nickname='', email=''):
        query = '''
            SELECT about, email, fullname, nickname
            FROM users
            WHERE {};
        '''

        condition = ''

        if nickname and email:
            condition = 'nickname = \'{}\' OR email = \'{}\''.format(nickname, email)
        elif nickname:
            condition = 'nickname = \'{}\''.format(nickname)
        elif email:
            condition = 'email = \'{}\''.format(email)

        return self.db_socket.execute_query(query.format(condition))

    def update_user(self, nickname, email='', fullname='', about=''):
        query_template = '''
            UPDATE users SET {}
            WHERE nickname='{}'
            RETURNING about, email, fullname, nickname;
        '''

        update = ''

        if email:
            update += 'email = \'{}\''.format(email)

        if fullname:
            if update:
                update += ', '
            update += 'fullname = \'{}\''.format(fullname)

        if about:
            if update:
                update += ', '
            update += 'about = \'{}\''.format(about)

        query = query_template.format(update, nickname)

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'about': db_object.get('about'),
            'email': db_object.get('email'),
            'fullname': db_object.get('fullname'),
            'nickname': db_object.get('nickname'),
        }


user_model = UserModel()
