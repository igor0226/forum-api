from .base import BaseModel


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

    def create_posts(self, posts):
        query = '''
            INSERT INTO posts
            (
              created, isEdited, message, parent,
              forum, thread, author
            )
            VALUES
        '''

        for post in posts:
            query += '''
                ({}, {}, '{}', {}, '{}', {}, '{}'),
            '''.format(
                post.get('created'),
                'TRUE' if post.get('isEdited') == 'True' else 'FALSE',
                post.get('message'),
                post.get('parent'),
                post.get('forum'),
                post.get('thread'),
                post.get('author'),
            )

        query += '''
            RETURNING id, created, isEdited, message,
            parent, forum, thread, author;
        '''

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'id': db_object.get('id'),
            'created': db_object.get('created'),
            'isEdited': db_object.get('isEdited'),
            'message': db_object.get('message'),
            'parent': db_object.get('parent'),
            'forum': db_object.get('forum'),
            'thread': db_object.get('thread'),
            'author': db_object.get('author'),
        }


post_model = PostModel()
