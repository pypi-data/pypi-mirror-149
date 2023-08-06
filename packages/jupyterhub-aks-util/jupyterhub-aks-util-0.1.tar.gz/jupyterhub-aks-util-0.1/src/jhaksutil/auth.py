import json
import requests

class AzureBearerToken:
    def __init__(self, tenant_id, client_id, client_secret):
        self.token = self._get_token(tenant_id, client_id, client_secret)

    def __repr__(self):
        return self.token

    def __str__(self):
        return self.token

    def _get_token(self, tenant_id: str, client_id: str, client_secret: str) -> str:
        resp = requests.post(
            url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "resource": "https://management.azure.com/",
            }
        )
        token_data = json.loads(resp.text)
        return token_data["access_token"]
