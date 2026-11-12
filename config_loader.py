import os
import json

DEFAULT_CONFIG = {
    "paths": {
        "custom_tc_excel": "test_cases.xlsx",
        "artifacts_dir": "artifacts",
        "screenshots_dir": "artifacts/screenshots"
    },
    "quality_gate": {
        "min_pass_score": 85
    },
    "browser": {
        "headless": False,
        "slow_mo_ms": 500,
        "timeout_ms": 10000
    }
}

def load_config(config_path: str = "config.json") -> dict:
    if not os.path.exists(config_path):
        return DEFAULT_CONFIG
    with open(config_path, "r", encoding="utf-8") as f:
        user_cfg = json.load(f)

    return {
        "paths": {**DEFAULT_CONFIG["paths"], **user_cfg.get("paths", {})},
        "quality_gate": {**DEFAULT_CONFIG["quality_gate"], **user_cfg.get("quality_gate", {})},
        "browser": {**DEFAULT_CONFIG["browser"], **user_cfg.get("browser", {})}
    }