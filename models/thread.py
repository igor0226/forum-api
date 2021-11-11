from jinja2 import Template
from models.base import BaseModel
from models.helpers import (
    serialize_pg_timestamp,
)


class ThreadModel(BaseModel):
    def get_thread(self, slug, thread_id=None):
        slug_is_valid = slug and isinstance(slug, str)
        thread_is_valid = thread_id is not None and isinstance(thread_id, int)

        query = Template('''
            SELECT id, message, author, created, forum, slug, title, votes
            FROM threads
            WHERE
            {% if slug_is_valid %}
              slug = '{{ thread_slug }}'
            {% endif %}
            {% if slug_is_valid and thread_is_valid  %}
              OR
            {% endif %}
            {% if thread_is_valid %}
              id = {{ thread_id }}
            {% endif %}
            ;
        ''').render(
            thread_slug=slug,
            thread_id=thread_id,
            slug_is_valid=slug_is_valid,
            thread_is_valid=thread_is_valid,
        )

        return self.db_socket.execute_query(query)

    def insert_thread(self, author, forum, message, title, votes,
                      thread_id=None, created=None,
                      slug=None):
        query = Template('''
            INSERT INTO threads
            (author, forum, message, title, votes
              {% if has_thread %}, id{% endif %}
              {% if created %}, created{% endif %}
              {% if slug %}, slug{% endif %}
            )
            VALUES (
              '{{ author }}',
              '{{ forum }}',
              '{{ message }}',
              '{{ title }}',
              {{ votes }}
              {% if has_thread %}, {{ thread_id }} {% endif %}
              {% if created %}, '{{ created }}' {% endif %}
              {% if slug %}, '{{ slug }}'{% endif %}
            )
            RETURNING id, author, created, forum,
            slug, title, votes, message;
        ''').render(
            author=author,
            forum=forum,
            message=message,
            title=title,
            votes=votes,
            thread_id=thread_id,
            has_thread=thread_id is not None,
            created=created,
            slug=slug,
        )

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
