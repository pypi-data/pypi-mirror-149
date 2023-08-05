from typing import List


class User:
    def __init__(self, email, admin):
        self.email = email
        self.admin = admin


class Organization:
    id: str
    name: str
    auth_type: str
    users: List[User]

    def __init__(self, doc):
        names = doc.to_dict()
        self.id = doc.id
        self.name = names['name']
        self.auth_type = names['auth_type']
        self.users = list(map(lambda user: User(user['email'], user.get('admin', False)), names['users']))
