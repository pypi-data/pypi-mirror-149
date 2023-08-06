import logging
import os
import typing

from mlfoundry.tracking.auth_service import AuthService
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore

TRACKING_TOKEN_ENV_VAR = "MLFLOW_TRACKING_TOKEN"
API_KEY_ENV_VAR = "MLF_API_KEY"

logger = logging.getLogger(__name__)


class Session:
    def __init__(
        self, auth_service: AuthService, tracking_service: TruefoundryRestStore
    ):
        self.auth_service: AuthService = auth_service
        self.tracking_service: TruefoundryRestStore = tracking_service
        self._api_key: typing.Optional[str] = None

    def _reset_session(self):
        self._api_key = None
        os.environ.pop(TRACKING_TOKEN_ENV_VAR, None)

    def init_session(
        self,
        api_key: typing.Optional[str] = None,
    ):
        self._reset_session()

        tenant_id = self.tracking_service.get_tenant_id()

        if api_key is not None:
            self._api_key = api_key
        elif API_KEY_ENV_VAR in os.environ:
            self._api_key = os.environ[API_KEY_ENV_VAR]

        if self._api_key is None:
            logger.info(
                "Session was not set as api key was neither passed, not set via env var"
            )
            return

        token = self.auth_service.get_token(api_key=self._api_key, tenant_id=tenant_id)
        os.environ[TRACKING_TOKEN_ENV_VAR] = token
