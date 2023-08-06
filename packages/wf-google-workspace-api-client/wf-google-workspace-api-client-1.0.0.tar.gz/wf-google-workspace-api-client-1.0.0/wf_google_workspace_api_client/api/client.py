import json
import logging
from typing import Union
from uuid import UUID

import requests
from requests.adapters import HTTPAdapter, Retry

from .. import const
from ..models.user import GWorkspaceUser
from ..models.watch import GWorkspaceWatch, CreateWatch, DeleteWatch

logger = logging.getLogger(__name__)


class Api:
    def __init__(
        self,
        audience: str = const.WF_AUTH0_GOOGLE_WORKSPACE_API_AUDIENCE,
        auth_domain: str = const.WF_AUTH0_DOMAIN,
        client_id: str = const.WF_AUTH0_CLIENT_ID,
        client_secret: str = const.WF_AUTH0_CLIENT_SECRET,
        api_url: str = const.WF_GOOGLE_WORKSPACE_API_URL,
    ):
        self.audience = audience
        self.auth_domain = auth_domain
        self.auth_url = f"https://{self.auth_domain}".rstrip("/")

        self.client_id = client_id
        self.client_secret = client_secret

        self.api_url = api_url.rstrip("/")
        self.session = self._init_request_retry_object()
        self.access_token = self._load_access_token()

    def _init_request_retry_object(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    def _load_access_token(self):
        response = self.session.post(
            url=f"{self.auth_url}/oauth/token",
            data=json.dumps(
                {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "audience": self.audience,
                    "grant_type": "client_credentials",
                }
            ),
            headers={"content-type": "application/json"},
        )

        data = response.json()
        return data["access_token"]

    def request(self, method, path, params: dict = None, data: Union[dict, bytes] = None):
        url = f"{self.api_url}/{path}"

        d = data
        if isinstance(data, dict):
            d = json.dumps(data).encode("utf-8")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=d,
                headers={"content-type": "application/json", "authorization": f"Bearer {self.access_token}"},
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            logger.exception(f"Request HTTPError ({err.response.status_code}): {url}")
            raise err
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"Request ConnectionError: {url}")
            raise err
        except requests.exceptions.Timeout as err:
            logger.exception(f"Request Timeout: {url}")
            raise err
        except requests.exceptions.RequestException as err:
            logger.exception(f"Unexpected RequestException ({err.response.status_code}): {url}")
            raise err

    def get(self, path, params: dict = None):
        response = self.request(method="GET", path=path, params=params)
        return response.json()

    def post(self, path, params: dict = None, data: dict = None):
        response = self.request(method="POST", path=path, params=params, data=data)
        return response.json()

    def delete(self, path, params: dict = None, data: dict = None):
        response = self.request(method="DELETE", path=path, params=params, data=data)
        return response.json()

    def get_user_by_email(self, email) -> GWorkspaceUser:
        r = self.get(f"users/{email}")
        user = GWorkspaceUser.parse_obj(r)
        return user

    def create_user_watch(self, uuid: UUID, url: str, token: str, ttl: int) -> GWorkspaceWatch:
        r = self.post("users/watch", data=CreateWatch(uuid=uuid, url=url, token=token, ttl=ttl).dict())
        watch = GWorkspaceWatch.parse_obj(r)
        return watch

    def delete_watch(self, uuid: UUID, resource_id: str):
        r = self.delete("/", data=DeleteWatch(uuid=uuid, resource_id=resource_id))
        return r
