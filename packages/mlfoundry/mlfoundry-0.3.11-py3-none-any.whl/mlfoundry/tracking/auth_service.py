from mlflow.utils.rest_utils import MlflowHostCreds, http_request_safe

AUTH_SERVER_URL = "https://auth-server.tfy-ctl-us-east-1-develop.develop.truefoundry.io"


class AuthService:
    def __init__(self, auth_server_url: str = AUTH_SERVER_URL):
        self.host_creds = MlflowHostCreds(host=auth_server_url)

    def get_token(self, api_key: str, tenant_id: str) -> str:
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint="/api/v1/oauth/api-keys/token",
            method="post",
            json={"apiKey": api_key, "clientId": tenant_id},
        )
        response = response.json()
        token = response["accessToken"]
        return token
