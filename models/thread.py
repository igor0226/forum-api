from .base import BaseModel


class ThreadModel(BaseModel):
    def get_thread(self, slug, thread_id=None):
        query = '''
            SELECT id, author, created, forum, slug, title, votes
            FROM threads
            WHERE slug = \'{}\''''.format(slug)

        if thread_id is not None:
            query += ' OR id ={}'.format(thread_id)

        query += ';'

        return self.db_socket.execute_query(query)

    def insert_thread(self, author, forum, message, title, votes,
                      thread_id=None, created=None,
                      slug=None):
        insert_part = '''
            INSERT INTO threads
            (author, forum, message, title, votes'''
        values_part = '''
            VALUES ('{}', '{}', '{}', '{}', {}'''.format(
            author,
            forum,
            message,
            title,
            votes,
        )
        returning_part = '''
            RETURNING id, author, created, forum, slug, title, votes, message;
        '''

        if thread_id:
            insert_part += ', id'
            values_part += ', {}'.format(thread_id)

        if created:
            insert_part += ', created'
            values_part += ', \'{}\''.format(created)

        if slug:
            insert_part += ', slug'
            values_part += ', \'{}\''.format(slug)

        insert_part += ')'
        values_part += ')'

        query = insert_part + values_part + returning_part

        return self.db_socket.execute_query(query)

    def get_threads_by_forum(self, slug, limit=None):
        query = '''
                SELECT id, author, created, forum, message, slug, title, votes
                FROM threads
                WHERE slug = '{}'
        '''.format(slug)

        if limit is not None:
            query += 'LIMIT {}'.format(limit)

        query += ';'

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        created = ''

        # 2021-03-07 01:04:50.105000-00-00 ->
        # 2021-03-07T01:04:50.105Z
        if db_object.get('created'):
            created = str(db_object.get('created'))
            created = created[:10:] + 'T' + created[11::]
            created = created[:-9:] + 'Z'

        return {
            'id': db_object.get('id'),
            'author': db_object.get('author'),
            'created': created,
            'forum': db_object.get('forum'),
            'message': db_object.get('message'),
            'slug': db_object.get('slug'),
            'title': db_object.get('title'),
            'votes': db_object.get('votes'),
        }


thread_model = ThreadModel()
