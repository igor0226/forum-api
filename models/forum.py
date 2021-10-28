from .base import BaseModel


class ForumModel(BaseModel):
    def get_forum(self, slug):
        query = '''
            SELECT posts, slug, threads, title, author FROM forums
            WHERE slug = '{}';
        '''.format(slug)

        return self.db_socket.execute_query(query)

    def create_forum(self, slug, title, author, posts=0, threads=0):
        query = '''
            INSERT INTO forums
            (slug, title, author, posts, threads)
            VALUES ('{}', '{}', '{}', {}, {})
            RETURNING slug, title, author, posts, threads;
        '''.format(slug, title, author, posts, threads)

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'posts': db_object.get('posts'),
            'slug': db_object.get('slug'),
            'threads': db_object.get('threads'),
            'title': db_object.get('title'),
            'user': db_object.get('author'),
        }


forum_model = ForumModel()
