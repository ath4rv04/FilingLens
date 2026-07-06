from pydantic import BaseModel
from filinglens.settings import CORS_ORIGINS


class APIConfig(BaseModel):
    title: str = "FilingLens-IN API"
    description: str = (
        "Production-grade multimodal financial filing intelligence backend."
    )
    version: str = "3.0"
    cors_origins: list[str] = CORS_ORIGINS


api_settings = APIConfig()
