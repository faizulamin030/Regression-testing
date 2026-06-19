import json
import random
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Set


class DataGenerator:
    _rrn_lock = threading.Lock()
    _rrn_registry_path: Optional[Path] = None
    _rrn_registry_loaded = False
    _rrn_registry: Set[str] = set()
    _rrn_last_second = ""
    _rrn_counter = 0

    @classmethod
    def configure_rrn_registry(cls, registry_path: Path) -> None:
        with cls._rrn_lock:
            cls._rrn_registry_path = registry_path
            cls._rrn_registry_loaded = False
            cls._rrn_registry = set()
            cls._rrn_last_second = ""
            cls._rrn_counter = 0

    @classmethod
    def _load_rrn_registry(cls) -> None:
        if cls._rrn_registry_loaded:
            return

        cls._rrn_registry = set()
        if cls._rrn_registry_path and cls._rrn_registry_path.exists():
            try:
                with cls._rrn_registry_path.open("r", encoding="utf-8") as handle:
                    data = json.load(handle)
                values = data.get("rrns", []) if isinstance(data, dict) else data
                cls._rrn_registry = {
                    str(value)
                    for value in values
                    if str(value).isdigit() and len(str(value)) == 12
                }
            except (OSError, json.JSONDecodeError):
                cls._rrn_registry = set()
        cls._rrn_registry_loaded = True

    @classmethod
    def _save_rrn_registry(cls) -> None:
        if not cls._rrn_registry_path:
            return

        cls._rrn_registry_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"rrns": sorted(cls._rrn_registry)}
        with cls._rrn_registry_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

    @classmethod
    def generate_rrn(cls) -> str:
        with cls._rrn_lock:
            cls._load_rrn_registry()

            while True:
                now = datetime.now()
                second_key = now.strftime("%j%H%M%S")
                if second_key != cls._rrn_last_second:
                    cls._rrn_last_second = second_key
                    cls._rrn_counter = 0

                if cls._rrn_counter > 999:
                    time.sleep(0.001)
                    continue

                candidate = f"{second_key}{cls._rrn_counter:03d}"
                cls._rrn_counter += 1
                if candidate in cls._rrn_registry:
                    continue

                cls._rrn_registry.add(candidate)
                cls._save_rrn_registry()
                return candidate

    @staticmethod
    def generate_stan() -> str:
        return "".join(str(random.randint(0, 9)) for _ in range(6))

    @staticmethod
    def today_date(fmt: str = "%Y-%m-%d") -> str:
        return datetime.now().strftime(fmt)

    @staticmethod
    def current_time(fmt: str = "%H:%M:%S") -> str:
        return datetime.now().strftime(fmt)

    @staticmethod
    def current_datetime(fmt: str = "%Y%m%d%H%M%S") -> str:
        return datetime.now().strftime(fmt)

    @classmethod
    def generate_rtp_id(cls) -> str:
        return f"rtp-{cls.generate_rrn()}-{cls.generate_stan()}"

    @classmethod
    def default_tokens(cls) -> Dict[str, str]:
        return {
            "RRN": cls.generate_rrn(),
            "STAN": cls.generate_stan(),
            "DATE": cls.today_date(),
            "TIME": cls.current_time(),
            "DATETIME": cls.current_datetime(),
            "RTP_ID_UNIQUE": cls.generate_rtp_id(),
        }
