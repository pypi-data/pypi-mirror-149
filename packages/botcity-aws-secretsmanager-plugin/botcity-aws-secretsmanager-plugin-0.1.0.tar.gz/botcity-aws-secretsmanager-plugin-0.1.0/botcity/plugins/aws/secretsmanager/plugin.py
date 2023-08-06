import boto3
import json
import base64
from typing import Union, Dict, Optional, List
from .utils import secret_not_found_handler


class BotSecretsManagerPlugin:
    RAISE_IF_NOT_FOUND = False

    def __init__(self, region_name: str = 'us-east-1', use_credentials_file: Optional[bool] = True,
                 access_key_id: Optional[str] = None, secret_access_key: Optional[str] = None) -> None:
        """
        BotSecretsManagerPlugin

        Args:
            region_name (str, optional): Default region when creating new connections.
            use_credentials_file (bool, optional): If set to True will make
                authentication via AWS credentials file.
            access_key_id (str, optional): AWS access key ID.
            secret_access_key (str, optional): AWS secret access key.
        """
        self._bucket_name = None
        if use_credentials_file:
            self._client = boto3.client(service_name='secretsmanager')
        else:
            self._client = boto3.client(
                service_name='secretsmanager',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name
            )

    @property
    def secrets_client(self):
        """
        Returns the aws client instance.

        Returns:
            secretsmanager_instance: The aws client instance.
        """
        return self._client

    def create_secret(self, secret_name: str, secret_value: Union[str, Dict], description: str, **kwargs) -> Dict:
        """
        Creates a new secret.
        
        [See documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.create_secret)

        Args:
            secret_name (str): The name of the new secret.
            secret_value (str or Dict): The secret value, can be dict or string.
            description (str): The description of the secret.

        Returns:
            secret: Returns the secret info.
        """  # noqa
        if isinstance(secret_value, dict):
            secret_value = json.dumps(secret_value)
        return self._client.create_secret(Name=secret_name, SecretString=secret_value, Description=description,
                                          **kwargs)

    def list_secrets(self, **kwargs) -> List:
        """
        Lists the secrets that are stored by Secrets Manager.
        
        [See documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.list_secrets)
        
        Returns:
            secrets: The list of secrets.
        """  # noqa
        response = self._client.list_secrets(**kwargs)
        return response["SecretList"]

    @secret_not_found_handler
    def describe_secret(self, secret_name: str, **kwargs) -> Union[Dict, None]:
        """
        Retrieves the details of a secret.

        [See documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.describe_secret)

        Args:
            secret_name (str): The ARN or name of the secret.

        Returns:
            secret_info: Return the dict with the secret info or None if secret not exists.
        """  # noqa
        return self._client.describe_secret(SecretId=secret_name, **kwargs)

    @secret_not_found_handler
    def get_secret_value(self, secret_name: str, **kwargs) -> Union[str, None]:
        """
        Retrieves the secret value.
        
        [See documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value)

        Args:
            secret_name (str): The ARN or name of the secret to retrieve.

        Returns:
            value: The secret value or None if secret not exists.
        """  # noqa
        response = self._client.get_secret_value(SecretId=secret_name, **kwargs)
        if "SecretString" in response:
            return response["SecretString"]
        else:
            return base64.b64decode(response["SecretBinary"]).decode("utf-8")

    @secret_not_found_handler
    def update_secret(self, secret_name: str, secret_value: Union[str, Dict], description: str = None,
                      **kwargs) -> Union[Dict, None]:
        """
        Modifies the details of a secret, including metadata and the secret value.
        
        [See documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.update_secret)
        
        Args:
            secret_name (str): The ARN or name of the secret
            secret_value (str or Dict): The new secret value.
            description (str, optional): The new description of the secret.

        Returns:
            secret: Return the secret info or None if secret not exists.
        """  # noqa
        if isinstance(secret_value, dict):
            secret_value = json.dumps(secret_value)

        if description:
            kwargs["Description"] = description

        return self._client.update_secret(SecretId=secret_name, SecretString=secret_value, **kwargs)

    @secret_not_found_handler
    def delete_secret(self, secret_name: str, without_recovery: bool = False, **kwargs) -> Union[Dict, None]:
        """
        Deletes a secret and all of its versions.
        
        [See documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.delete_secret)
        
        Args:
            secret_name (str): The ARN or name of the secret.
            without_recovery (bool, optional): Delete the secret without any recovery window.

        Returns:
            secret: Returns the secret info or None if secret not exists.
        """  # noqa
        return self._client.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=without_recovery,
                                          **kwargs)

    def __getitem__(self, item: str) -> Union[Dict, None]:
        return self.get_secret_value(secret_name=item)

    def __setitem__(self, key: str, value: Union[str, Dict]) -> None:
        self.create_secret(secret_name=key, secret_value=value, description='')

    def __delitem__(self, key: str):
        self.delete_secret(secret_name=key)
