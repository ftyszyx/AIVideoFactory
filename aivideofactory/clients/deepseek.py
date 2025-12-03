++ aivideofactory/clients/deepseek.py
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx


class DeepSeekError(RuntimeError):
    """Raised when the DeepSeek API returns an error or malformed payload."""


@dataclass
class DeepSeekClient:
    api_key: str
    api_base: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    timeout_seconds: float = 30.0

    def generate_storyboard_payload(self, prompt: str, scene_count: int, language: str) -> dict[str, Any]:
        system_prompt = (
            "You are an assistant that produces structured JSON storyboards for short videos. "
            "Respond only with JSON in UTF-8 without additional commentary."
        )
        user_prompt = (
            f"用户原始提示词：{prompt}\n"
            f"请基于该提示词构思一个短视频脚本，包含{scene_count}个分镜。"
            "返回JSON，字段包括overview, scenes。overview为整体介绍，scenes为数组，"
            "每个元素包含id, title, description, duration_seconds, camera_notes。"
            f"请使用{language}书写。"
        )
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"}
        }

    def call_chat_completions(self, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{self.api_base.rstrip('/')}/v1/chat/completions"
        try:
            response = httpx.post(url, headers=headers, json=payload, timeout=self.timeout_seconds)
        except httpx.HTTPError as exc:
            raise DeepSeekError(f"Failed to reach DeepSeek API: {exc}") from exc
        if response.status_code >= 400:
            raise DeepSeekError(f"DeepSeek API error {response.status_code}: {response.text}")
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise DeepSeekError("DeepSeek API returned invalid JSON") from exc

    def extract_content(self, body: dict[str, Any]) -> str:
        try:
            choice = body["choices"][0]
            content = choice["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise DeepSeekError("Unexpected DeepSeek response structure") from exc
        if not isinstance(content, str) or not content.strip():
            raise DeepSeekError("DeepSeek response content is empty")
        return content

    def parse_json_content(self, content: str) -> dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            parts = cleaned.split("\n", 1)
            if len(parts) == 2:
                cleaned = parts[1]
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise DeepSeekError("DeepSeek response is not valid JSON") from exc

    def generate_storyboard(self, prompt: str, scene_count: int, language: str = "中文") -> dict[str, Any]:
        payload = self.generate_storyboard_payload(prompt=prompt, scene_count=scene_count, language=language)
        body = self.call_chat_completions(payload)
        content = self.extract_content(body)
        return self.parse_json_content(content)

