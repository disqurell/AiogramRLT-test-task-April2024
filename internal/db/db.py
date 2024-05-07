from pydantic_settings import BaseSettings


class MongoConfig(BaseSettings):
    # Если вы случайно нашли этот репозиторий,
    # помните: никакого хардкода для конфигураций!
    # Это тестовый пример. Тут можно)

    MONGO_HOST: str = "localhost"
    MONGO_USER: str = "mongoadmin"
    MONGO_PORT: int = 27017
    MONGO_PASS: str = "mongoadminpass"
    MONGO_DB: str = "sampleDB"

    def build_uri(self):
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}:{self.MONGO_PORT}"


MONGO_CONFIG = MongoConfig()
