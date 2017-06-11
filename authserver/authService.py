from flask_restful import fields, marshal_with

user_fields = {
        'id': fields.Integer,
        'email': fields.String}

class AuthService:
    _users = {}

    @marshal_with(user_fields)
    def check_user_password(self, email, password, provider='local'):
        if email in self._users and \
                self._users[email]['password'] == password and \
                self._users[email]['provider'] == provider:
            return {
                'email': email,
                'id': self._users[email]['id']}
        return {}

    def check_user(self, email, provider='local'):
        return email in self._users and \
                self._users[email]['provider'] == provider

    def get_user(self, email):
        return self._users.get(email, {})

    def create_user(self, email, password, provider='local'):
        if not self._users:
            _id = 1
        else:
            _id = max(map(lambda x: x['id'], self._users.values())) + 1
        _new_user = dict(
                email=email,
                password=password,
                provider=provider,
                id=_id)
        self._users[email] = _new_user

authService = AuthService()

