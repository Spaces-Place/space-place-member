from time import time
from fastapi import HTTPException, status
from jose import jwt
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv


env_file = '.env.development' if os.getenv('APP_ENV') == 'development' else '.env.production'
load_dotenv(env_file)

ssm = boto3.client('ssm', region_name='ap-northeast-2')

def get_parameter_from_ssm(name: str) -> str:
    try:
        parameter = ssm.get_parameter(Name=name , WithDecryption=True)
    except ssm.exceptions.ParameterNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} parameter does not exist in AWS SSM."
        )
    except ssm.exceptions.InvalidKeyId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid KMS key used for decrypting {name}."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve {name} from AWS SSM: {e}"
        )
    
    key = parameter.get("Parameter", {}).get("Value")
    if key is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} parameter is missing or has no value."
        )

    return key

def get_config_value(name: str) -> str:
    if env_file == '.env.development':
        value = os.getenv(name)
        if value is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{name} environment variable is missing."
            )
        return value
    return get_parameter_from_ssm(name)

def get_user_db_username() -> str:
    return get_config_value("USER_DB_USERNAME")

def get_user_db_name() -> str:
    return get_config_value("USER_DB_NAME")

def get_user_db_host() -> str:
    return get_config_value("USER_DB_HOST")

def get_user_db_password() -> str:
    return get_config_value("USER_DB_PASSWORD")

def get_jwt_secret_key() -> str:
    return get_config_value("USER_JWT_SECRET")