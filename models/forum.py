from .base import BaseModel


class ForumModel(BaseModel):
    def get_forum(self, slug):
        query = '''
            SELECT posts, slug, threads, title, author FROM forums
            WHERE slug = '{}';
        '''.format(slug)

        return self.db_socket.execute_query(query)


forum_model = ForumModel()
