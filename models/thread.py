from models.base import BaseModel
from models.helpers import serialize_pg_timestamp


class ThreadModel(BaseModel):
    def get_thread(self, slug, thread_id=None):
        query = '''
            SELECT id, message, author, created, forum, slug, title, votes
            FROM threads
            WHERE
        '''

        slug_appended = False
        if slug is not None and isinstance(slug, str):
            query += 'slug = \'{}\''.format(slug)
            slug_appended = True

        if thread_id is not None and isinstance(thread_id, int):
            if slug_appended:
                query += ' OR'
            query += ' id = {}'.format(thread_id)

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

    def get_threads_by_forum(self, slug, limit=None, since=None, desc=None):
        query = '''
        SELECT id, author, created, forum, message, slug, title, votes
        FROM threads
        WHERE forum = '{}'
        '''.format(slug)

        operator = '<=' if desc == 'true' else '>='

        if since is not None:
            query += 'AND created {} \'{}\''.format(operator, since)
    
        query += '\nORDER BY created'.format(limit)

        if desc == 'true':
            query += ' DESC'.format(limit)

        if limit is not None:
            query += '\nLIMIT {}'.format(limit)
    
        query += ';'
    
        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'id': db_object.get('id'),
            'author': db_object.get('author'),
            'created': serialize_pg_timestamp(
                db_object.get('created'),
            ),
            'forum': db_object.get('forum'),
            'message': db_object.get('message'),
            'slug': db_object.get('slug'),
            'title': db_object.get('title'),
            'votes': db_object.get('votes'),
        }


thread_model = ThreadModel()
