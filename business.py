from data import users


def get_user_by_email(email):
    # password is ignored
    return [user for user in users if email == user.get('email')][0]