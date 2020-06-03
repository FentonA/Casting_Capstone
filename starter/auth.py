from os import environ
import json 
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urlib.requests import urlopen

AUTH0_DOMAIN = 'dev-hsnuo.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENNCE = #Capstone

##AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code)
    self.error = error 
    self.status_code = status_code

##Auth Header 
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
    }, 401)
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorizaion header must with the Bearer'
    }, 401)
    elif len(parts) == 1:
        raise AuthError({
        'code': 'Invalid_header',
        'description': 'Token not found'
    }, 401)
    elif len(parts) > 2:
        raise AuthError({
        'code': 'invalid_header',
        'description': 'Authorization needs Bearer token' 
    }, 401)

    def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid claims',
            'description':'Permssion not inlcuded in this payload'
    }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': "You don't have permission to access this"
    }, 401)
    
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks  = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverfied_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
    }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid':key['kid'],
                'use':key['use'],
                'n': key['n'],
                'e':key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
        }, 401)

        except jwt.JWTClaimError:
            raise AuthError({
            'code': 'token_expired',
            'description': 'Incorrect claims, please check the audienc and issuer'
        }, 401)

        except Exception:
            raise AuthError({
            'code': 'invalid header',
            'descripion': 'Unable to parse authentication token'
        }, 400)
    raise AuthError({
        'code': "invalid header",
        'description': 'Unable to find the appropriate key'
}, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
