from __future__ import print_function

import logging
from typing import List

from googleapiclient.errors import HttpError
from xenon_gcp_sdk.cloudfirestore import cloud_firestore_service

from ..api.organization import Organization
from ..api.user_identifier import UserIdentifier


def get_people(firebase_client, org: Organization):
    try:
        for user in org.users:
            auth_token = None
            if org.auth_type == 'personal':
                auth_token = get_token_by_email(firebase_client, user.email)
                if not auth_token:
                    continue
            yield UserIdentifier(organization_id=org.id,
                                 email=user.email,
                                 auth_token=auth_token,
                                 admin=user.admin)
    except HttpError as err:
        logging.info('failed to get people of {name} organization/n error: {error}'.format(name=org.name, error=err))


def get_all_emails(firebase_client) -> List[UserIdentifier]:
    for organization in list(get_organizations(firebase_client)):
        yield from get_people(firebase_client, organization)


def get_token_by_email(firebase_client, email):
    tokens = cloud_firestore_service.get_by_id(firebase_client, 'oauth_tokens', email)
    if tokens:
        return tokens[-1].to_dict()
    else:
        logging.error(f'missing token for personal user: {email}')
        return {}


def get_organizations(firebase_client):
    for org in list(map(lambda doc: Organization(doc),
                        cloud_firestore_service.get_all(firebase_client, 'organizations'))):
        yield org
