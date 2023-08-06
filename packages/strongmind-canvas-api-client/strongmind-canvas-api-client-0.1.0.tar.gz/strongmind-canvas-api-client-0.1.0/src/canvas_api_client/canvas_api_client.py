from botocore.exceptions import ClientError
import requests
from .secrets_manager import SecretsManager
from .exceptions import APIKeyNotFoundError, DomainNameNullError
import json


class CanvasApiClient:
    def __init__(self, domain, version='v1', **kwargs):
        api_token = kwargs.get('api_token')
        secrets_library = kwargs.get('secrets_library')
        secret = kwargs.get('secret')
        self.domain = domain
        self.version = version
        self.api_key = self.get_api_key(api_token=api_token, secret=secret, secrets_library=secrets_library)
        self.base_url = f"https://{self.domain}/api/{version}"

    def get_api_key(self, **kwargs):
        api_token = kwargs.get('api_token')
        secret = kwargs.get('secret')
        secrets_library = kwargs.get('secrets_library')

        if api_token:
            return api_token
        if secret and secrets_library:
            return CanvasApiClient.get_specific_api_token(secret, secrets_library)
        return CanvasApiClient.get_default_api_token(self.domain)

    def get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.api_key),
            'Content-Type': 'application/json'
        }

    def get_paginated_response(self, path):
        current_response = self.get(path)
        final_response = current_response.json()
        while "next" in current_response.links:
            next_url = current_response.links['next']['url'].replace(f"{self.base_url}/", "")
            current_response = self.get(next_url)
            final_response.extend(current_response.json())
        return final_response

    def get(self, path):
        response = requests.get(
            f"{self.base_url}/{path}",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response

    def get_json(self, path):
        return self.get(path).json()

    def put(self, path, body):
        response = requests.put(
            f"{self.base_url}/{path}",
            headers=self.get_headers(),
            json=body
        )
        response.raise_for_status()
        return response

    def post(self, path, body):
        response = requests.post(
            f"{self.base_url}/{path}",
            headers=self.get_headers(),
            json=body
        )
        response.raise_for_status()
        return response

    def post_graphql(self, body):
        response = requests.post(
            f"https://{self.domain}/api/graphql",
            headers=self.get_headers(),
            json=body
        )
        response.raise_for_status()
        return response

    def delete(self, path, body=None):
        if body:
            response = requests.delete(
                f"{self.base_url}/{path}",
                headers=self.get_headers(),
                json=body
            )
        else:
            response = requests.delete(
                f"{self.base_url}/{path}",
                headers=self.get_headers()
            )
        response.raise_for_status()
        return response

    @staticmethod
    def get_default_api_token(domain_name):
        """
        Get the right API key from secrets manager
        """
        secret = json.loads(SecretsManager.get('canvas_api_keys'))
        if domain_name == "":
            raise DomainNameNullError("domain_name can't be None")

        if domain_name in secret:
            return secret[domain_name]
        else:
            raise APIKeyNotFoundError(f"{domain_name} not found in secrets manager.")

    @staticmethod
    def get_specific_api_token(secret, secrets_library):
        try:
            returned_secret = json.loads(SecretsManager.get(secrets_library)).get(secret)
            if not returned_secret:
                raise APIKeyNotFoundError(f"Invalid Secret Key: {secret}")

        except ClientError:
            raise APIKeyNotFoundError(f"Invalid Secret: {secrets_library}")

        return returned_secret
