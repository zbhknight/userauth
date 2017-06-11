from flask import Flask, jsonify, request, make_response
from flask import current_app
from flask import Blueprint
from flask.views import MethodView
from flask_restful import reqparse
from flask_jwt_extended import JWTManager, jwt_required, \
        create_access_token, get_jwt_claims

from authService import authService, user_fields

auth_bp = Blueprint('auth', __name__)

LoginParser = reqparse.RequestParser()
LoginParser.add_argument('email', type=str, required=True, 
        help='Email is required')
LoginParser.add_argument('password', type=str, required=True, 
        help='Password is required')

class Login(MethodView):
    
    @staticmethod
    def setLoginResponse(user):
        _user = dict(user)
        _user['token'] = create_access_token(
                identity=user['id'])
        return dict(
                status='success',
                user=_user)

    def post(self):
        args = LoginParser.parse_args()
        try:
            _user = authService.check_user_password(
                    args['email'], args['password'])
            if _user['id']:
                response = Login.setLoginResponse(_user)
                ret_code = 200
            else:
                response = dict(
                        status='fail',
                        message='Email or password errror')
                ret_code = 404
        except Exception as e:
            response = dict(
                    status='fail',
                    message=str(e))
            ret_code = 500
        return make_response(jsonify(response)), ret_code

class Register(MethodView):
    def post(self):
        args = LoginParser.parse_args()
        if authService.check_user(args['email']):
            response = dict(
                    status='fail',
                    message='User exists')
            return make_response(jsonify(response)), 401

        try:
            authService.create_user(args['email'], args['password'])
            response = dict(
                    status='success')
            ret_code = 201
        except Exception as e:
            response = dict(
                    status='fail', message=str(e))
            ret_code = 500
        return make_response(jsonify(response)), ret_code

login_view = Login.as_view('login')
register_view = Register.as_view('register')

auth_bp.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth_bp.add_url_rule('/auth/register', view_func=register_view,
        methods=['POST'])
