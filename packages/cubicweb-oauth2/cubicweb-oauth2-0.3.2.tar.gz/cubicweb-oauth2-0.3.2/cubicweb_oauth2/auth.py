# copyright 2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import html

from authlib.integrations.requests_client import OAuth2Session
from authlib.jose import jwt
import requests
from pyramid.authentication import IAuthenticationPolicy
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPBadRequest,
    HTTPUnauthorized,
)
from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import remember
from zope.interface import implementer

from cubicweb import NoResultError
from cubicweb.pyramid.config import get_random_secret_key
from cubicweb.server.utils import crypt_password


@view_config(route_name="oauth2-start", permission=NO_PERMISSION_REQUIRED)
def start(request):
    rd = request.params.get("rd") or "/"
    return HTTPFound(request.registry["oauth2"].create_authorization_url(request, rd))


@view_config(route_name="oauth2-callback", permission=NO_PERMISSION_REQUIRED)
def callback(request):
    try:
        state = request.params["state"]
    except KeyError:
        raise HTTPBadRequest("missing state")
    try:
        rd = request.params["rd"]
    except KeyError:
        raise HTTPBadRequest("missing rd parameter")
    token = request.registry["oauth2"].fetch_token(request, state, rd)
    config = request.registry["cubicweb.config"]
    user_login = token[config["oauth2-token-login"]]
    with request.registry["cubicweb.repository"].internal_cnx() as cnx:
        try:
            user = cnx.find("CWUser", login=user_login).one()
        except NoResultError:
            if not config["oauth2-register-user"]:
                raise HTTPUnauthorized("no such user in database")
            kwargs = {
                key: token[config["oauth2-token-{}".format(key)]]
                for key in ("firstname", "surname", "email")
            }
            email = kwargs.pop("email")
            try:
                address = cnx.find("EmailAddress", address=email).one()
            except NoResultError:
                address = cnx.create_entity("EmailAddress", address=email)
            group = cnx.find("CWGroup", name=config["oauth2-default-group"]).one()
            user = cnx.create_entity(
                "CWUser",
                login=user_login,
                upassword=crypt_password(get_random_secret_key()),
                in_group=group,
                use_email=address,
                primary_email=address,
                **kwargs
            )
            cnx.commit()
        eid = user.eid

    return HTTPFound(
        request.params["rd"],
        headers=remember(request, eid),
    )


class Oauth2:
    def __init__(
        self,
        client_id,
        client_secret,
        server_url=None,
        authorization_url=None,
        token_url=None,
        jwk_path=None,
    ):
        if not server_url and (not authorization_url or not token_url or not jwk_path):
            raise ValueError(
                (
                    "You should either set `url` or all "
                    "`authorization_url`, `token_url` and `jwk_path`"
                )
            )
        self._client_id = client_id
        self._client_secret = client_secret
        self._server_url = server_url
        self._authorization_url = authorization_url
        self._token_url = token_url
        self._session = self._create_session()
        if jwk_path:
            with open(jwk_path) as f:
                self._jwk = f.read()
        else:
            self._jwk = None

    def _create_session(self, state=None):
        return OAuth2Session(
            self._client_id,
            self._client_secret,
            scope="openid email profile",
            state=state,
        )

    def _read_openid_configuration(self):
        resp = requests.get(
            self._server_url.rstrip("/") + "/.well-known/openid-configuration",
        )
        resp.raise_for_status()
        config = resp.json()
        if not self._authorization_url:
            self._authorization_url = config["authorization_endpoint"]
        if not self._token_url:
            self._token_url = config["token_endpoint"]
        if not self._jwk:
            resp = requests.get(config["jwks_uri"])
            resp.raise_for_status()
            self._jwk = resp.json()

    @property
    def authorization_url(self):
        if not self._authorization_url:
            self._read_openid_configuration()
        return self._authorization_url

    @property
    def token_url(self):
        if not self._token_url:
            self._read_openid_configuration()
        return self._token_url

    @property
    def jwk(self):
        if not self._jwk:
            self._read_openid_configuration()
        return self._jwk

    def create_authorization_url(self, request, rd):
        redirect_uri = request.route_url("oauth2-callback", _query={"rd": rd})
        auth_url, state = self._session.create_authorization_url(
            self.authorization_url,
            redirect_uri=redirect_uri,
        )
        request.session["_oauth2_state"] = state
        return auth_url

    def fetch_token(self, request, state, rd):
        if state != request.session.get("_oauth2_state"):
            raise HTTPBadRequest("invalid state")
        del request.session["_oauth2_state"]
        redirect_uri = request.route_url("oauth2-callback", _query={"rd": rd})
        session = self._create_session(state)
        resp = session.fetch_token(
            self.token_url,
            authorization_response=request.url,
            redirect_uri=redirect_uri,
        )
        token = jwt.decode(resp["id_token"], self.jwk)
        return token


@implementer(IAuthenticationPolicy)
class Oauth2AuthenticationPolicy:
    def authenticated_userid(self, request):
        """
        When `oauth2-force-login` is set, force authentication by
        redirecting unauthenticated requests to /oauth2/start
        """
        if not request.registry["cubicweb.config"]["oauth2-force-login"]:
            return
        if request.authorization and request.authorization.authtype == "Cubicweb":
            # do not block signed requests from cwclientlib
            return
        if request.path in {
            request.route_path(r) for r in ("oauth2-callback", "oauth2-start")
        }:
            return
        raise HTTPUnauthorized(
            body=(
                "<!DOCTYPE html><html><head>"
                '<meta http-equiv="refresh" content="0; url={}" />'
                "</head></html>"
            ).format(
                html.escape(
                    request.route_url(
                        "oauth2-start",
                        _query={"rd": request.url},
                    )
                )
            )
        )

    def effective_principals(self, request):
        return ()

    def remember(self, request, principal, **kw):
        return ()

    def forget(self, request):
        return ()


def includeme(config):
    cwconfig = config.registry["cubicweb.config"]
    config.registry["oauth2"] = Oauth2(
        cwconfig["oauth2-client-id"],
        cwconfig["oauth2-client-secret"],
        server_url=cwconfig["oauth2-server-url"],
        authorization_url=cwconfig["oauth2-authorization-url"],
        token_url=cwconfig["oauth2-token-url"],
        jwk_path=cwconfig["oauth2-jwk-path"],
    )
    policy = Oauth2AuthenticationPolicy()
    config.registry["cubicweb.authpolicy"]._policies.append(policy)
    config.add_route("oauth2-start", "/oauth2/start")
    config.add_route("oauth2-callback", "/oauth2/callback")
    config.scan(__name__)
