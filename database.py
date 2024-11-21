from sqlmodel import Session, create_engine, text
from utils.aws_config import get_aws_config


aws_config = get_aws_config()
db_config = aws_config.get_db_config()

user_db_host = db_config['host']
user_db_name = db_config['db_name']
user_db_username = db_config['username']
user_db_password = db_config['password']

engine_url = create_engine(
    f"mysql+mysqlconnector://{user_db_username}:{user_db_password}@{user_db_host}:3306/{user_db_name}",
    echo=True,
)


def conn():
    import os

    sql_file_path = os.path.join(os.path.dirname(__file__), "setup.sql")
    session = next(get_session())
    with open(sql_file_path, "r", encoding="utf-8") as file:
        sql_script = file.read()
        session.execute(text(sql_script))
    session.commit()


def get_session():
    with Session(engine_url) as session:
        yield session
