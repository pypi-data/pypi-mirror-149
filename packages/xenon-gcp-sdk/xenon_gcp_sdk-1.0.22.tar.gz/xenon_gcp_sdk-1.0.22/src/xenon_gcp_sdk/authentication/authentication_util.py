from flask import Response
from google.auth.transport import requests
from google.oauth2 import id_token

from .authentication_error import TokenError, AuthorizationError


def verify_pubsub_token(pubsub_token, app_config_token):
    if pubsub_token != app_config_token:
        err = TokenError(f'Invalid token: {pubsub_token}')
        return Response(f"{err}", status=500, mimetype='application/json')


def verify_authorization(func, bearer_token, service_account_email):
    try:
        token = bearer_token.split(' ')[1]
        claim = id_token.verify_oauth2_token(token, requests.Request())
        if claim["email"] == service_account_email and claim["email_verified"] is True:
            return func()
        else:
            err = AuthorizationError(f'AuthorizationError: Invalid email: {claim["email"]}')
            return Response(f"{err}", status=500, mimetype='application/json')
    except BaseException as e:
        return Response(f"{e}", status=500, mimetype='application/json')


def ignore_dev_env(func, host):
    if host.startswith('localhost'):
        return func
