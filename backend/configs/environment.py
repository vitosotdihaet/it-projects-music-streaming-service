from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_PORT: int
    MINIO_WEBUI_PORT: int
    MINIO_MUSIC_BUCKET: str
    MINIO_COVER_BUCKET: str

    ACCOUNTS_ROOT_USER: str
    ACCOUNTS_ROOT_PASSWORD: str
    ACCOUNTS_DB: str
    ACCOUNTS_PORT: int

    MUSIC_ROOT_USER: str
    MUSIC_ROOT_PASSWORD: str
    MUSIC_DB: str
    MUSIC_PORT: int

    USER_ACTIVITY_ROOT_USER: str
    USER_ACTIVITY_ROOT_PASSWORD: str
    USER_ACTIVITY_DB: str
    USER_ACTIVITY_PORT: int

    BACKEND_PORT: int

    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_ADMIN_SECRET_KEY: str
    AUTH_ACCESS_TOKEN_EXPIRED_MINUTES: int

    FRONTEND_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
