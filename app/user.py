from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Example users
users = {
    "user1": User("1", "user1", "password1"),
    "user2": User("2", "user2", "password2")
} 