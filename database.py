from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, text
from utils.aws_ssm_key import get_user_db_name, get_user_db_host, get_user_db_password

password = get_user_db_password()
user_db_host = get_user_db_host()
user_db_name = get_user_db_name()
engine_url = create_engine(
    f"mysql+mysqlconnector://root:{password}@{user_db_host}:3306/{user_db_name}",
    echo=True,
)


def conn():
    # SQLModel.metadata.create_all(engine_url)

    import os

    sql_file_path = os.path.join(os.path.dirname(__file__), "setup.sql")
    session = next(get_session())
    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()
        session.execute(text(sql_script))
    session.commit()
    pass


def get_session():
    with Session(engine_url) as session:
        yield session
