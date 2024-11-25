import os
import boto3
from typing import Dict

from utils.aws_ssm import ParameterStore
from utils.env_config import get_env_config
from utils.credential import Credential
from utils.database_config import DatabaseConfig


class AWSService:

    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AWSService, cls).__new__(cls)
            
        return cls._instance
    
    def __init__(self):
        self._env_config = get_env_config()
        self._credentials = Credential.get_credentials()
        self._parameter_store = ParameterStore()
        self._database_config = DatabaseConfig()

    # 서비스별 client 생성
    def create_client(self, service_name: str):
        return boto3.client(
            service_name,
            aws_access_key_id=self._credentials.access_key,
            aws_secret_access_key=self._credentials.secret_key,
            region_name=self._credentials.region
        )

    # JWT
    def get_jwt_secret(self) -> str:
        if self._env_config.is_development:
            return os.getenv('USER_JWT_SECRET')
        
        return self._parameter_store.get_parameter("USER_JWT_SECRET")
    
def get_aws_service() -> AWSService:
    return AWSService()