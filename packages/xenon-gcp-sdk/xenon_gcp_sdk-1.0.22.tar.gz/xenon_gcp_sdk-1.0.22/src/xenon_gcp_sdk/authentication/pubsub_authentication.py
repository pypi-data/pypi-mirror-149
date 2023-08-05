import functools

from .authentication_util import verify_pubsub_token, verify_authorization
from ..secretmanager import secret_manager_service
from flask import request


def pubsub_authentication(func):
    @functools.wraps(func)
    def verify():
        if request.host.startswith('localhost'):
            return func()
        authorization = request.headers.get('Authorization')
        request_token = request.args.get('token', '')
        app_config_token = secret_manager_service.get_secret('pubsub_token')
        return verify_pubsub_token(
            request_token,
            app_config_token) or verify_authorization(func,
                                                      authorization,
                                                      secret_manager_service.get_secret('service_account_email'))

    return verify
