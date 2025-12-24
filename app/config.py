from dataclasses import dataclass


@dataclass
class Settings:
    host: str = "127.0.0.1"
    port: int = 5002
    title: str = "Async Serving Main API"


settings = Settings()
