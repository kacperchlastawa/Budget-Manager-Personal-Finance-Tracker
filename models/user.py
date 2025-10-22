from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, email, password, name):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.name = name
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def change_password(self, old_password,new_password):
        if not self.check_password(old_password):
            raise ValueError("Old password is incorrect.")
        self.password_hash = generate_password_hash(new_password)

    def check_password_strength(self, password):
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True




