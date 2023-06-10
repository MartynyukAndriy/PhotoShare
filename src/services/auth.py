from typing import Optional

from src.database.db import get_db


class Auth:

    def verify_password(self, plain_password, hashed_password):
        pass

    def get_password_hash(self, password: str):
        pass

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        pass

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        pass

    async def decode_refresh_token(self, refresh_token: str):
        pass

    async def get_current_user(self, token, db):
        pass

    def create_email_token(self, data: dict):
        pass

    async def get_email_from_token(self, token: str):
        pass


auth_service = Auth()
