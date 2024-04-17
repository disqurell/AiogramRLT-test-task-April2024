from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import logging
from aiogram import Bot, Dispatcher


class Settings(BaseSettings):
    bot_token: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class BotHelper:
    def __init__(self) -> None:
        self.bot = None
        self.dp = None

    def run(self):
        logging.basicConfig(level=logging.INFO)
        # Объект бота
        self.bot = Bot(token=config.bot_token.get_secret_value())
        # Диспетчер
        self.dp = Dispatcher()

    def get_dp(self):
        if self.dp is None:
            raise Exception("Dispatcher is not initialized")
        return self.dp

    def get_bot(self):
        if self.bot is None:
            raise Exception("Bot is not initialized")
        return self.bot


config = Settings()

bot = BotHelper()
