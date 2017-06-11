from flask import Flask, jsonify, request, make_response
from flask import Blueprint
from flask_restful import Api, Resource, url_for
from flask_jwt_extended import JWTManager, jwt_required, \
        create_access_token, get_jwt_claims

from authService import authService
from auth import auth_bp
from oauth import oauth_bp

app = Flask(__name__)
app.secret_key = "secret"
jwt = JWTManager(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class User(Resource):

    #@jwt_required
    def get(self):
        return authService._users, 200

api.add_resource(User, '/auth/users')

app.register_blueprint(auth_bp)
app.register_blueprint(oauth_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)
