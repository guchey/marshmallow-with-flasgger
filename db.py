_users_data = []


class Users(object):

    @staticmethod
    def all():
        return _users_data

    @staticmethod
    def save(user):
        _users_data.append(user)
        return user
