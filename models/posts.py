from models.base import BaseModel
from models.helpers import get_pg_timestamp, serialize_pg_timestamp


class PostModel(BaseModel):
    def get_post(self, post_id):
        query = '''
            SELECT id, created, isEdited, message,
            parent, forum, thread, author
            FROM posts
            WHERE id = '{}';
        '''.format(post_id)

        return self.db_socket.execute_query(query)

    def get_non_existing_posts(self, post_ids):
        query = 'SELECT id FROM get_non_existing_posts(ARRAY['

        for i, post_id in enumerate(post_ids):
            if i:
                query += ', '

            query += str(post_id)

        query += ']::integer[]);'

        return self.db_socket.execute_query(query)

    def create_posts(self, posts, thread_id, forum_slug):
        default_timestamp = get_pg_timestamp()
        query = '''
            INSERT INTO posts
            (
              created, isEdited, message, parent,
              forum, thread, author
            )
            VALUES
        '''

        for i, post in enumerate(posts):
            post_forum = post.get('forum')
            post_forum = f'\'{post_forum}\'' if post_forum else f'\'{forum_slug}\''

            query += '''
                ('{}', {}, '{}', {}, {}, {}, '{}')'''.format(
                post.get('created') or default_timestamp,
                'TRUE' if post.get('isEdited') == 'true' else 'FALSE',
                post.get('message'),
                post.get('parent') or 'NULL',
                post_forum,
                post.get('thread') or thread_id,
                post.get('author'),
            )
            if i < len(posts) - 1:
                query += ','

        query += '''
            RETURNING id, created, isEdited, message,
            parent, forum, thread, author;
        '''

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'id': db_object.get('id'),
            'created': serialize_pg_timestamp(
                db_object.get('created'),
            ),
            'isEdited': db_object.get('isEdited'),
            'message': db_object.get('message'),
            'parent': db_object.get('parent'),
            'forum': db_object.get('forum'),
            'thread': db_object.get('thread'),
            'author': db_object.get('author'),
        }


post_model = PostModel()
