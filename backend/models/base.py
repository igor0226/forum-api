from db_socket import db_socket


class BaseModel:
    def __init__(self):
        self.db_socket = db_socket
