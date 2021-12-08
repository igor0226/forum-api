from jinja2 import Template
from models.base import BaseModel
from models.helpers import (
    get_pg_timestamp,
    serialize_pg_timestamp,
    get_first_defined,
)


class PostModel(BaseModel):
    def get_post(self, post_id):
        query = Template('''
            SELECT id, created, isEdited, message,
            parent, forum, thread, author, pathArray
            FROM posts
            WHERE id = '{{ post_id }}';
        ''').render(post_id=post_id)

        return self.db_socket.execute_query(query)

    def get_non_existing_posts(self, post_ids):
        query = Template('''
                    SELECT id FROM get_non_existing_posts(
                      ARRAY[
                          {% for i, post_id in post_ids %}
                            {{ post_id }}
                            {% if posts_len > 1 and i < posts_len - 1 %},{% endif %}
                          {% endfor %}
                      ]::integer[]
                    );
                ''').render(
            post_ids=enumerate(post_ids),
            posts_len=len(post_ids),
        )

        return self.db_socket.execute_query(query)

    @staticmethod
    def _patch_posts(posts, thread_id, forum_slug):
        patched_posts = []
        default_ts = get_pg_timestamp()
        for post in posts:
            created = post.get('created') or default_ts
            is_edited = 'TRUE' if post.get('isEdited') == 'true' else 'FALSE'
            parent = post.get('parent') or 'NULL'
            forum = get_first_defined(post.get('forum'), forum_slug)
            thread = get_first_defined(post.get('thread'), thread_id)

            patched_posts.append({
                **post,
                'created': created,
                'isEdited': is_edited,
                'parent': parent,
                'forum': forum,
                'thread': thread,
            })

        return patched_posts

    def create_posts(self, posts, thread_id, forum_slug):
        patched_posts = self._patch_posts(
            posts,
            thread_id,
            forum_slug,
        )

        query = Template('''
            INSERT INTO posts
            (
              created, isEdited, message, parent,
              forum, thread, author
            )
            VALUES
            {% for i, post in posts %}
              (
                '{{ post.get('created') }}',
                {{ post.get('isEdited') }},
                '{{ post.get('message') }}',
                {{ post.get('parent') or 'NULL' }},
                '{{ post.get('forum') }}',
                {{ post.get('thread') }},
                '{{ post.get('author') }}'
              )
              {% if posts_len > 1 and i < posts_len - 1 %},{% endif %}
            {% endfor %}
            RETURNING id, created, isEdited, message,
            parent, forum, thread, author;
        ''').render(
            posts=enumerate(patched_posts),
            posts_len=len(patched_posts),
        )

        return self.db_socket.execute_query(query)

    def get_parent_thread(self, thread_id, limit, desc=False, since_path=None):
        query = Template('''
            SELECT parent, innerRootPost, pathArray
            FROM posts
            WHERE thread = '{{ thread_id }}' AND parent IS NULL
            {% if has_since_path %}
                AND pathArray {{ operator }} ARRAY{{ since_path }}::BIGINT[]
            {% endif %}
            ORDER BY innerRootPost {% if desc %} DESC {% endif %}
            LIMIT {{ limit }} + 1;
        ''').render(
            thread_id=thread_id,
            limit=limit,
            desc=desc,
            operator='<' if desc else '>',
            has_since_path=since_path is not None,
            since_path=since_path,
        )

        return self.db_socket.execute_query(query)

    def get_thread_posts(self, thread_id, limit, sort, desc, since, since_path, limit_path):
        query = Template('''
            SELECT id, created, isEdited, message,
            parent, forum, thread, author, innerRootPost, pathArray
            FROM posts
            WHERE thread = {{ thread_id }}

            {% if has_since %}
                {% if sort == 'flat' %}
                    AND id {{ operator }} {{ since }}
                {% elif sort == 'tree' or sort == 'parent_tree' %}
                    AND pathArray {{ operator }} ARRAY{{ since_path }}::BIGINT[]
                {% endif %}
            {% endif %}

            {% if sort == 'parent_tree' and has_limit %}
                AND pathArray {{ inverted_operator }} ARRAY{{ limit_path }}::BIGINT[]
            {% endif %}

            {% if sort == 'flat' %}
                ORDER BY {% if desc %} id DESC {% else %} id {% endif %}
            {% elif sort == 'tree' %}
                ORDER BY pathArray {% if desc %} DESC {% endif %}
            {% elif sort == 'parent_tree' %}
                ORDER BY {% if desc %} innerRootPost DESC, pathArray ASC {% else %} pathArray {% endif %}
            {% endif %}

            {% if has_limit and sort != 'parent_tree' %} LIMIT {{ limit }} {% endif %};
        ''').render(
            thread_id=thread_id,
            has_limit=limit is not None,
            limit=limit,
            sort=sort,
            operator='<' if desc else '>',
            inverted_operator='>' if desc else '<',
            desc=desc,
            has_since=since is not None,
            since=since,
            since_path=since_path,
            limit_path=limit_path,
        )

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'id': db_object.get('id'),
            'created': serialize_pg_timestamp(
                timestamp=db_object.get('created'),
            ),
            'isEdited': db_object.get('isEdited'.lower()),
            'message': db_object.get('message'),
            'parent': db_object.get('parent'),
            'forum': db_object.get('forum'),
            'thread': db_object.get('thread'),
            'author': db_object.get('author'),
            'pathArray': db_object.get('patharray'),
        }


post_model = PostModel()
