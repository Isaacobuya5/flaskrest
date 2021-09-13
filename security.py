from werkzeug.security import safe_str_cmp
from models.user import UserModel


# authenticates the user


def authenticate(username, password):
    # user = username_mapping.get(username, None)  # default value None
    # now retrieving user from database
    user = UserModel.find_by_username(username)
    # safe comaprison of strings even with encodings
    if user and safe_str_cmp(user.password, password):
        return user

# called when we send a request with the jwt token


def identity(payload):
    user_id = payload["identity"]
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
