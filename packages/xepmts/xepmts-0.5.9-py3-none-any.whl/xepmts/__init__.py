"""Top-level package for xepmts."""

__author__ = """Yossi Mosbacher"""
__email__ = 'joe.mosbacher@gmail.com'
__version__ = '0.5.9'

from getpass import getpass
import xeauth
from xepmts.db.client import default_client, get_admin_client
from xepmts.db.client import get_client as _get_client
from . import streams
from .settings import config

def login(version='v2',
          username=None,
          password=None,
          token=None, 
          scopes=["openid profile email offline_access read:all"],
          auth_kwargs={},
          **kwargs):
    auth_kwargs = dict(auth_kwargs)
    audience = auth_kwargs.pop('audience', config.OAUTH_AUDIENCE)

    if token is not None:
        xetoken = xeauth.token.XeToken(access_token=token)
    elif username is not None:
        xetoken = xeauth.user_login(username=username, password=password, scopes=scopes, audience=audience, **auth_kwargs )
    elif version=='v2':
        xetoken = xeauth.login(scopes=scopes, audience=audience, **auth_kwargs)
    else:
        token = getpass.getpass('API Token: ')
        xetoken = xeauth.token.XeToken(access_token=token)
    try:
        if xetoken.expired:
            xetoken.refresh_tokens()
    except:
        pass
    return _get_client(version, xetoken=xetoken, **kwargs)

get_client = login

def settings(**kwargs):
    from eve_panel import settings as panel_settings
    if not kwargs:
        return dir(panel_settings)
    else:
        for k,v in kwargs.items():
            setattr(panel_settings, k, v)

def extension():
    import eve_panel
    eve_panel.extension()

notebook = extension