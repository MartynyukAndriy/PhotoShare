from pydantic import BaseSettings


class Settings(BaseSettings):

    sqlalchemy_database_url: str = "postgresql+psycopg2://postgres:123456@localhost:5432/postgres"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"
    mail_username: str = "example@mail.com"
    mail_password: str = "password"
    mail_from: str = "example@mail.com"
    mail_port: int = 123
    mail_server: str = "smtp.mail.com"
    redis_host: str = "localhost"
    redis_port: int = 6379
    cloudinary_name: str = "name"
    cloudinary_apy_key: str = "123456"
    cloudinary_apy_secret: str = "secret"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
