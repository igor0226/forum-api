from jinja2 import Template
from models.base import BaseModel
from models.helpers import (
    serialize_pg_timestamp,
    make_kv_list,
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
            SELECT author, thread, vote
            FROM thread_votes
            WHERE author = '{{ author }}' AND
            thread = '{{ thread_id }}';
        ''').render(
            author=author,
            thread_id=thread_id,
        )

        return self.db_socket.execute_query(query)

    def update_thread_vote(self, thread_id, nickname, vote):
        query = Template('''
            UPDATE thread_votes
            SET vote = {{ vote }}
            WHERE author = '{{ author }}' AND
            thread = {{ thread_id }};
        ''').render(
            author=nickname,
            thread_id=thread_id,
            vote=vote,
        )

        return self.db_socket.execute_query(query)

    def add_thread_vote(self, thread_id, nickname, vote):
        query = Template('''
            INSERT INTO thread_votes
            (author, thread, vote)
            VALUES ('{{ author }}', {{ thread_id }}, {{ vote }});
        ''').render(
            author=nickname,
            thread_id=thread_id,
            vote=vote,
        )

        return self.db_socket.execute_query(query)

    def modify_thread(self, thread_id, thread_slug, message, title, created):
        fields = make_kv_list(
            message=message,
            title=title,
            created=created,
        )

        query = Template('''
            UPDATE threads SET

            {% for i, field in fields %}
              {{ field.key }} = '{{ field.value }}'
              {% if fields_len > 1 and i < fields_len - 1 %},{% endif %}
            {% endfor %}

            WHERE
            {% if thread_id_is_valid %}
              id = {{ thread_id }}
            {% else %}
              slug = '{{ thread_slug }}'
            {% endif %}

            RETURNING id, message, author, created,
            forum, slug, title, votes;
        ''').render(
            thread_id=thread_id,
            thread_id_is_valid=thread_id is not None,
            thread_slug=thread_slug,
            fields=enumerate(fields),
            fields_len=len(fields),
        )

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'id': db_object.get('id'),
            'author': db_object.get('author'),
            'created': serialize_pg_timestamp(
                timestamp=db_object.get('created'),
            ),
            'forum': db_object.get('forum'),
            'message': db_object.get('message'),
            'slug': db_object.get('slug'),
            'title': db_object.get('title'),
            'votes': db_object.get('votes'),
        }


thread_model = ThreadModel()
