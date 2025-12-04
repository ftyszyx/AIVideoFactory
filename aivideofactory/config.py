++aivideofactory / config.py
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AIVF_", env_file=".env", extra="ignore")

    deepseek_api_key: str = Field(..., min_length=1, repr=False)
    deepseek_api_base: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    default_scene_count: int = Field(6, ge=1, le=20)
    output_root: Path = Path("runs")
    output_format: Literal["json"] = "json"

    @computed_field
    @property
    def output_root_resolved(self) -> Path:
        return self.output_root.expanduser().resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.output_root_resolved.mkdir(parents=True, exist_ok=True)
    return settings
