import json
from typing import Any, Dict, Optional


class ResponseValidator:
    def __init__(self, validation_logger) -> None:
        self.validation_logger = validation_logger

    def validate(
        self,
        validation_type: str,
        expected_result: str,
        response: Dict[str, Any],
        validation_rules: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        validation_type = (validation_type or "response").strip().lower()
        rules = validation_rules or {}

        if validation_type == "status_code":
            return self._validate_status_code(expected_result, response)
        if validation_type == "json_field":
            return self._validate_json_field(expected_result, response, rules)
        if validation_type == "response":
            return self._validate_response_contains(expected_result, response)

        self.validation_logger.warning("Unknown validation_type=%s; fallback to response", validation_type)
        return self._validate_response_contains(expected_result, response)

    def _validate_status_code(self, expected_result: str, response: Dict[str, Any]) -> Dict[str, Any]:
        expected_code = int(str(expected_result).strip())
        actual_code = response.get("status_code")
        passed = actual_code == expected_code
        actual = str(actual_code)
        self.validation_logger.info(
            "STATUS_CODE_VALIDATION | expected=%s | actual=%s | passed=%s",
            expected_code,
            actual,
            passed,
        )
        return {"passed": passed, "actual": actual}

    def _validate_json_field(
        self,
        expected_result: str,
        response: Dict[str, Any],
        validation_rules: Dict[str, Any],
    ) -> Dict[str, Any]:
        body = response.get("body", {})
        field_path = validation_rules.get("field")

        if not field_path:
            if ":" in expected_result:
                field_path, expected_result = expected_result.split(":", 1)
            else:
                return {"passed": False, "actual": "Missing field rule for json_field validation"}

        actual_value = self._get_path_value(body, field_path.strip())
        expected_value = expected_result.strip()
        passed = str(actual_value) == expected_value
        self.validation_logger.info(
            "JSON_FIELD_VALIDATION | field=%s | expected=%s | actual=%s | passed=%s",
            field_path,
            expected_value,
            actual_value,
            passed,
        )
        return {"passed": passed, "actual": str(actual_value)}

    def _validate_response_contains(self, expected_result: str, response: Dict[str, Any]) -> Dict[str, Any]:
        # Normalize inputs
        expected = str(expected_result).strip()
        text = response.get("text", "") or ""
        body = response.get("body", {})
        body_text = json.dumps(body, ensure_ascii=False)

        # Backward-compat: if expected is a single message (no commas), use substring match.
        if "," not in expected:
            passed = expected in text or expected in body_text
            actual = body_text if len(body_text) <= 1000 else body_text[:1000] + "..."
            self.validation_logger.info(
                "RESPONSE_VALIDATION | expected_contains=%s | passed=%s",
                expected,
                passed,
            )
            return {"passed": passed, "actual": actual}

        # Helper: collect all string leaf values from the body (dicts/lists) so we
        # can split the actual message values reliably by commas even when the body
        # is JSON-encoded.
        def _collect_strings(node: Any) -> list:
            parts = []
            if isinstance(node, str):
                parts.append(node)
            elif isinstance(node, dict):
                for v in node.values():
                    parts.extend(_collect_strings(v))
            elif isinstance(node, list):
                for item in node:
                    parts.extend(_collect_strings(item))
            else:
                # convert other leaf types to string
                if node is not None:
                    parts.append(str(node))
            return parts

        # 1. Split expected into normalized set of messages
        expected_parts = [p.strip().lower() for p in expected.split(",")]
        expected_set = {p for p in expected_parts if p}

        # 2. Build actual message pool: include `text` and all string leaf values from `body`.
        actual_values = []
        if text:
            actual_values.append(text)
        actual_values.extend(_collect_strings(body))

        # Join the collected actual strings with commas and split to normalize messages.
        combined_actual_source = ",".join(actual_values)
        actual_parts = [p.strip().lower() for p in combined_actual_source.split(",")]
        actual_set = {p for p in actual_parts if p}

        # 3. Check that all expected messages appear among the actual messages (order-independent).
        passed = expected_set.issubset(actual_set)

        actual = body_text if len(body_text) <= 1000 else body_text[:1000] + "..."
        self.validation_logger.info(
            "RESPONSE_VALIDATION | expected_contains=%s | passed=%s",
            expected,
            passed,
        )
        return {"passed": passed, "actual": actual}

    @staticmethod
    def _get_path_value(payload: Any, path: str) -> Any:
        current = payload
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current
