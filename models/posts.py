from jinja2 import Template
from .base import BaseModel
from .helpers import (
    get_pg_timestamp,
    serialize_pg_timestamp,
    get_first_defined,
)


class PostModel(BaseModel):
    def get_post(self, post_id):
        query = Template('''
            SELECT id, created, isEdited, message,
            parent, forum, thread, author
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
                {{ post.get('parent') }},
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
