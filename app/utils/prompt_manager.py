from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class PromptManager:
    """data/prompts/ 의 .yml 파일을 로드해 content를 반환."""

    DEFAULT_PROMPTS_DIR = "data/prompts"

    def __init__(self, prompts_dir: Optional[str] = None):
        if prompts_dir is None:
            base = Path(__file__).resolve().parent.parent.parent
            prompts_dir = base / self.DEFAULT_PROMPTS_DIR
        self.prompts_dir = Path(prompts_dir)
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _load_yml(self, name: str) -> Dict[str, Any]:
        if name in self._cache:
            return self._cache[name]
        path = self.prompts_dir / f"{name}.yml"
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError(f"Invalid prompt yml (expected dict): {path}")
        self._cache[name] = data
        return data

    def get(self, name: str, **format_params: Any) -> str:
        data = self._load_yml(name)
        content = data.get("content")
        if content is None:
            raise ValueError(f"Prompt '{name}' has no 'content' key in {self.prompts_dir / (name + '.yml')}")
        text = content.strip()
        if format_params:
            text = text.format(**format_params)
        return text

    def list_prompts(self) -> list:
        if not self.prompts_dir.exists():
            return []
        return [p.stem for p in self.prompts_dir.glob("*.yml")]
