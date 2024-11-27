from dataclasses import dataclass
import os

from utils.aws_ssm import ParameterStore
from utils.env_config import get_env_config
from utils.mysqldb import MySQLDatabase
from utils.type.db_config_type import DBConfig

    
class DatabaseConfig:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConfig, cls).__new__(cls)

        return cls._instance

    """
    DB 환경에 따른 설정관리
    """
    def __init__(self):
        self._env_config = get_env_config()
        self._parameter_store = ParameterStore()

    def create_database(self) -> MySQLDatabase:
        db_config = self.get_db_config()
        print(f"db_config: {db_config}")
        return MySQLDatabase(db_config)

    def get_db_config(self) -> DBConfig:
        if self._env_config.is_development:
            return DBConfig(
                host=os.getenv('USER_DB_HOST'),
                dbname=os.getenv('USER_DB_NAME'),
                username=os.getenv('USER_DB_USERNAME'),
                password=os.getenv('USER_DB_PASSWORD')
            )
        else:
            return DBConfig(
                host=self._parameter_store.get_parameter("USER_DB_HOST"),
                dbname=self._parameter_store.get_parameter("USER_DB_NAME"),
                username=self._parameter_store.get_parameter("USER_DB_USERNAME"),
                password=self._parameter_store.get_parameter("USER_DB_PASSWORD", True)
            )