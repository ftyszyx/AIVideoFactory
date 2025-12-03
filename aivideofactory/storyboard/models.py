++ aivideofactory/storyboard/models.py
from __future__ import annotations

from typing import Iterable, List

from pydantic import BaseModel, Field, ValidationError


class StoryboardScene(BaseModel):
    id: int = Field(ge=0)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    duration_seconds: float = Field(gt=0)
    camera_notes: str | None = None


class Storyboard(BaseModel):
    prompt: str
    overview: str
    scenes: List[StoryboardScene]

    @classmethod
    def from_payload(cls, prompt: str, payload: dict) -> "Storyboard":
        try:
            raw_scenes = payload["scenes"]
            overview = payload["overview"]
        except KeyError as exc:
            raise ValueError("Storyboard payload missing required keys") from exc
        if not isinstance(raw_scenes, Iterable):
            raise ValueError("Storyboard scenes must be iterable")
        try:
            scenes = [StoryboardScene.model_validate(scene) for scene in raw_scenes]
        except ValidationError as exc:
            raise ValueError(f"Invalid scene structure: {exc}") from exc
        return cls(prompt=prompt, overview=overview, scenes=scenes)

    def to_serializable(self) -> dict:
        return {
            "prompt": self.prompt,
            "overview": self.overview,
            "scenes": [scene.model_dump() for scene in self.scenes]
        }

