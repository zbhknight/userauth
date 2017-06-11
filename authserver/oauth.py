import flask
from flask import Flask, jsonify, request, make_response
from flask import current_app
from flask import Blueprint
from flask.views import MethodView
from flask_restful import reqparse
from flask_jwt_extended import JWTManager, jwt_required, \
        create_access_token, get_jwt_claims
from oauth2client import client

from authService import authService
from auth import Login

oauth_bp = Blueprint('oauth', __name__)

Providers = {
    'google': {
        'secret_file': 'google_secret.json',
        'scope' : "https://www.googleapis.com/auth/userinfo.email",
        'callback': 'http://awsvps.com:4200/ngoauth/callback/google'
    }
}

def getAuthflow(providerName):
    if providerName not in Providers:
        return None
    return client.flow_from_clientsecrets(
            Providers[providerName]['secret_file'],
            scope=Providers[providerName]['scope'],
            redirect_uri=Providers[providerName]['callback']
            #include_granted_scopes=True)
            )

class OauthRedirect(MethodView):

    def get(self):
        provider = request.args.get('provider', 'google')
        provider = 'google' if provider == "" else provider
        authflow = getAuthflow(provider)
        auth_uri = authflow.step1_get_authorize_url()
        flask.session['provider'] = provider
        return flask.redirect(auth_uri)

class OauthCallback(MethodView):

    def get(self, provider):
        if 'code' not in request.args:
            return flask.redirect('/oauth/redirect?provider=%s' % provider)

        auth_code = request.args.get('code')
        authflow = getAuthflow(provider)

        try:
            credential = authflow.step2_exchange(auth_code)
        except Exception as e:
            response = dict(
                    status="fail",
                    message=str(e))
            return make_response(jsonify(response)), 500

        if credential and 'email' in credential.id_token:
            email = credential.id_token['email']
        else:
            return flask.redirect('/oauth/redirect?provider=%s' % provider)

        _user = authService.get_user(email)
        if _user and _user['provider'] != provider:
            response = dict(
                    status="fail",
                    message="User exists")
            return make_response(jsonify(response)), 401

        if not _user:
            authService.create_user(email, 'defaultpassword', provider)
        _user = authService.get_user(email)
        response = Login.setLoginResponse(_user)
        return make_response(jsonify(response)), 200

oauthredirect_view = OauthRedirect.as_view('oauthredirect')
oauthcallback_view = OauthCallback.as_view('oauthcallback')

oauth_bp.add_url_rule('/oauth/redirect', view_func=oauthredirect_view,
        methods=['GET'])
oauth_bp.add_url_rule('/oauth/callback/<provider>', view_func=oauthcallback_view,
        methods=['GET'])
