from jinja2 import Template
from models.base import BaseModel
from models.helpers import make_kv_list


class UserModel(BaseModel):
    def create_user(self, about, email, fullname, nickname):
        query = Template('''
            INSERT INTO users
            (about, email, fullname, nickname)
            VALUES (
                '{{ about }}',
                '{{ email }}',
                '{{ fullname }}',
                '{{ nickname }}'
            )
            RETURNING about, email, fullname, nickname;
        ''').render(
            about=about,
            email=email,
            fullname=fullname,
            nickname=nickname,
        )

        return self.db_socket.execute_query(query)

    # get user by nickname or email
    def get_users(self, nickname='', email=''):
        conditions = make_kv_list(
            nickname=nickname,
            email=email,
        )

        query = Template('''
            SELECT about, email, fullname, nickname
            FROM users
            WHERE
            {% for i, cond in conditions %}
              {{ cond.key }} = '{{ cond.value }}'
              {% if conditions_len > 1 and i < conditions_len - 1 %}
                OR
              {% endif %}
            {% endfor %}
        ''').render(
            conditions=enumerate(conditions),
            conditions_len=len(conditions),
        )

        return self.db_socket.execute_query(query)

    def update_user(self, nickname, email='', fullname='', about=''):
        fields = make_kv_list(
            email=email,
            fullname=fullname,
            about=about,
        )
        query = Template('''
            UPDATE users SET
            {% for i, field in fields %}
              {{ field.key }} = '{{ field.value }}'
              {% if fields_len > 1 and i < fields_len - 1 %},{% endif %}
            {% endfor %}
            WHERE nickname='{{ nickname }}'
            RETURNING about, email, fullname, nickname;
        ''').render(
            nickname=nickname,
            fields=enumerate(fields),
            fields_len=len(fields),
        )

        return self.db_socket.execute_query(query)

    def check_users_nicknames(self, nicknames):
        query = Template('''
            SELECT check_users_nicknames(ARRAY[
                {% for i, nickname in nicknames %}
                    '{{ nickname }}'
                    {% if nicknames_len > 1 and i < nicknames_len - 1 %},{% endif %}
                {% endfor %}
            ]::CITEXT[]) AS authors_exists;
        ''').render(
            nicknames=enumerate(nicknames),
            nicknames_len=len(nicknames),
        )

        return self.db_socket.execute_query(query)

    @staticmethod
    def serialize(db_object):
        return {
            'about': db_object.get('about'),
            'email': db_object.get('email'),
            'fullname': db_object.get('fullname'),
            'nickname': db_object.get('nickname'),
        }


user_model = UserModel()