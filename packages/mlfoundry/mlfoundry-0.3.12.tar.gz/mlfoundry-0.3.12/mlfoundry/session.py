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

    def init_session(
        self,
        api_key: typing.Optional[str] = None,
    ):
        tenant_id = self.tracking_service.get_tenant_id()

        final_api_key = api_key or os.getenv(API_KEY_ENV_VAR)

        if final_api_key is None:
            # if API key is not present,
            # then take a look if MLFLOW_TRACKING_TOKEN itself has been set.
            # this will be used in sfy.
            existing_token = os.getenv(TRACKING_TOKEN_ENV_VAR, "")
            if existing_token:
                logger.info("API key is not present. Using existing tracking token")
                return
            logger.info(
                "Session was not set as api key was neither passed, not set via env var"
            )
            return

        token = self.auth_service.get_token(api_key=final_api_key, tenant_id=tenant_id)
        os.environ[TRACKING_TOKEN_ENV_VAR] = token
