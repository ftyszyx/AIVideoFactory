++ aivideofactory/storyboard/generator.py
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from ..clients import DeepSeekClient, DeepSeekError
from ..config import get_settings
from .models import Storyboard


class StoryboardGenerator:
    def __init__(self, client: Optional[DeepSeekClient] = None):
        settings = get_settings()
        self._settings = settings
        self._client = client or DeepSeekClient(
            api_key=settings.deepseek_api_key,
            api_base=settings.deepseek_api_base,
            model=settings.deepseek_model
        )

    def run(self, prompt: str, scene_count: Optional[int] = None, language: str = "中文") -> Storyboard:
        count = scene_count or self._settings.default_scene_count
        if count < 1:
            raise ValueError("scene_count must be at least 1")
        try:
            payload = self._client.generate_storyboard(prompt=prompt, scene_count=count, language=language)
        except DeepSeekError as exc:
            raise RuntimeError(f"Storyboard generation failed: {exc}") from exc
        return Storyboard.from_payload(prompt=prompt, payload=payload)

    def save(self, storyboard: Storyboard, run_dir: Optional[Path] = None) -> Path:
        run_folder = run_dir or self._settings.output_root_resolved / datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        run_folder.mkdir(parents=True, exist_ok=True)
        target = run_folder / f"storyboard.{self._settings.output_format}"
        target.write_text(storyboard.model_dump_json(by_alias=True, indent=2, ensure_ascii=False), encoding="utf-8")
        return target


def generate_storyboard(prompt: str, scene_count: Optional[int] = None, language: str = "中文", run_dir: Optional[Path] = None) -> Path:
    generator = StoryboardGenerator()
    storyboard = generator.run(prompt=prompt, scene_count=scene_count, language=language)
    return generator.save(storyboard=storyboard, run_dir=run_dir)

