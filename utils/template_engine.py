import json
import re
from pathlib import Path
from typing import Any, Dict


PLACEHOLDER_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


class TemplateEngine:
    @staticmethod
    def load_json_template(request_file: Path) -> Any:
        with request_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @classmethod
    def render_template(cls, template_data: Any, values: Dict[str, Any]) -> Any:
        if isinstance(template_data, dict):
            return {
                key: cls.render_template(value, values)
                for key, value in template_data.items()
            }
        if isinstance(template_data, list):
            return [cls.render_template(item, values) for item in template_data]
        if isinstance(template_data, str):
            return cls._replace_placeholders(template_data, values)
        return template_data

    @staticmethod
    def _replace_placeholders(text: str, values: Dict[str, Any]) -> str:
        def replace(match: re.Match) -> str:
            token = match.group(1)
            return str(values.get(token, match.group(0)))

        return PLACEHOLDER_PATTERN.sub(replace, text)
