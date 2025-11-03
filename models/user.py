from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, username, email, password_hash, name):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.name = name
    @classmethod
    def create_new(cls, username,  password, email, name):
        password_hash = generate_password_hash(password)
        return cls(username, email, password_hash, name)
    
    def  verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def change_password(self, old_password,new_password):
        if not self.verify_password(old_password):
            raise ValueError("Old password is incorrect.")
        self.password_hash = generate_password_hash(new_password)




