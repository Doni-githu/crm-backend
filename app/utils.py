import json

from rest_framework_simplejwt.tokens import RefreshToken
import jwt

secret = 'awdadad'


def get_tokens_for_user(user):
    refresh = jwt.encode({'payload': user}, secret, algorithm="HS256")
    return refresh



def decode(token):
    jwt_options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }
    result = jwt.decode(
        token,
        secret,
        algorithms=['HS256'],
        verify=True,
    )

    return result
