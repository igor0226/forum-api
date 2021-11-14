from jinja2 import Template
from models.base import BaseModel
from models.helpers import (
    serialize_pg_timestamp,
)


class ThreadModel(BaseModel):
    def get_thread(self, slug, thread_id=None):
        thread_id_is_valid = thread_id is not None and isinstance(thread_id, int)

        query = Template('''
            SELECT id, message, author, created, forum, slug, title, votes
            FROM threads
            WHERE
            {% if thread_id_is_valid %}
              id = {{ thread_id }}
            {% else %}
              slug = '{{ thread_slug }}'
            {% endif %}
            ;
        ''').render(
            thread_slug=slug,
            thread_id=thread_id,
            thread_id_is_valid=thread_id_is_valid,
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
        query = Template('''
                SELECT id, author, created, forum, message, slug, title, votes
                FROM threads
                WHERE forum = '{{ slug }}'
                {% if since %}
                    AND created {{ operator }} '{{ since }}'
                {% endif %}
                ORDER BY created {% if is_desc %}DESC{% endif %}
                {% if has_limit %}
                    LIMIT {{ limit }}
                {% endif %}
                ;
        ''').render(
            slug=slug,
            since=since,
            operator='<=' if desc == 'true' else '>=',
            has_limit=limit is not None,
            limit=limit,
            is_desc=desc == 'true',
        )

        return self.db_socket.execute_query(query)

    def get_vote(self, author, thread_id):
        query = Template('''
            SELECT author, thread
            FROM thread_votes
            WHERE author = '{{ author }}'
            AND thread = '{{ thread_id }}';
        ''').render(
            author=author,
            thread_id=thread_id,
        )

        return self.db_socket.execute_query(query)

    def add_thread_vote(self, thread_id, nickname):
        query = Template('''
            INSERT INTO thread_votes
            (author, thread) VALUES ('{{ author }}', {{ thread_id }});
        ''').render(
            author=nickname,
            thread_id=thread_id,
        )

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
