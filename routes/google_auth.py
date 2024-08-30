from uuid import UUID

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from fastapi import APIRouter, Request, Depends
from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)

from auth.utils import create_access_token
from session.session import cookie, create_session, get_session, update_session

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"
CLIENT_CONFIG = {'web': {
    'client_id': os.getenv('GOOGLE_CLIENT_ID'),
    'project_id': os.getenv('GOOGLE_PROJECT_ID'),
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://www.googleapis.com/oauth2/v3/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
    'redirect_uris': os.getenv('GOOGLE_REDIRECT_URIS').split(','),
    'javascript_origins': os.getenv('GOOGLE_JAVASCRIPT_ORIGINS').split(',')
}}

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'oauth2'
API_VERSION = 'v2'

router = APIRouter()

@router.get('/token-google')
async def token_google(request: Request, session_id: UUID = Depends(cookie)):
    session = await get_session(session_id)
    if not session.credentials:
        return RedirectResponse(f'{request.url.scheme}://{request.url.hostname}:{request.url.port}/api/authorize')

    credentials = google.oauth2.credentials.Credentials(
      **session.credentials)

    user_info_service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    session.credentials = credentials_to_dict(credentials)
    await update_session(session_id, session)

    return JSONResponse({"access_token": create_access_token(user_info['email']), "token_type": "bearer"})


@router.get('/authorize')
async def authorize(request: Request):
      flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=CLIENT_CONFIG, scopes=SCOPES)
      flow.redirect_uri = f'{request.url.scheme}://{request.url.hostname}:{request.url.port}/api/oauth2callback'
      authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
      response = RedirectResponse(authorization_url)
      await create_session(state, response)
      return response


@router.get('/oauth2callback')
async def oauth2callback(request: Request, session_id: UUID = Depends(cookie)):
    session = await get_session(session_id)
    state = session.state
    flow = google_auth_oauthlib.flow.Flow.from_client_config(client_config=CLIENT_CONFIG, scopes=SCOPES, state=state)
    flow.redirect_uri = f'{request.url.scheme}://{request.url.hostname}:{request.url.port}/api/oauth2callback'
    authorization_response = str(request.url)

    if authorization_response[:5] != 'https':
      authorization_response = 'https' + authorization_response[4:]

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session.credentials = credentials_to_dict(credentials)
    await update_session(session_id, session)

    return RedirectResponse('/')

# @router.get('/revoke')
# async def revoke(session_id: UUID = Depends(cookie)):
#   session = await get_session(session_id)
#   # if 'credentials' not in flask.session:
#   if not session.credentials:
#     return ('You need to <a href="/authorize">authorize</a> before ' +
#             'testing the code to revoke credentials.')
#
#   credentials = google.oauth2.credentials.Credentials(
#     **flask.session['credentials'])
#
#   revoke = requests.post('https://oauth2.googleapis.com/revoke',
#       params={'token': credentials.token},
#       headers = {'content-type': 'application/x-www-form-urlencoded'})
#
#   status_code = getattr(revoke, 'status_code')
#   if status_code == 200:
#     return('Credentials successfully revoked.' + print_index_table())
#   else:
#     return('An error occurred.' + print_index_table())
#
#
# @router.get('/clear')
# async def clear_credentials():
#   if 'credentials' in flask.session:
#     del flask.session['credentials']
#   return ('Credentials have been cleared.<br><br>' +
#           print_index_table())


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
