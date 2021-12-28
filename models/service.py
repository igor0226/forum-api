from models.base import BaseModel


class ServiceModel(BaseModel):
    def get_all_tables_count(self):
        query = '''
            SELECT forums_len,
                posts_len,
                threads_len,
                users_len
            FROM get_all_tables_count();
        '''

        return self.db_socket.execute_query(query)

    def clear_all_tables(self):
        query = 'SELECT clear_all_tables() AS truncation_status;'

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'forum': db_object.get('forums_len'),
            'post': db_object.get('posts_len'),
            'thread': db_object.get('threads_len'),
            'user': db_object.get('users_len'),
        }


service_model = ServiceModel()
