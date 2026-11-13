import os
import json

CONFIG_FILE = "monitor_config.json"

DEFAULT_CONFIG = {
    "monitor_name": "Sentinel-QE Service & API Health Monitor",
    "port": 8900,
    "check_interval_sec": 5,
    "retry_threshold": 2,
    "timeout_sec": 3,
    "latency_warn_ms": 800,
    "artifacts_dir": "monitor_artifacts",
    "slack_webhook_url": "",
    "targets": [
        {"name": "SauceDemo Web", "url": "https://www.saucedemo.com/", "expected_status": 200},
        {"name": "GitHub API", "url": "https://api.github.com", "expected_status": 200}
    ]
}

def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        user_cfg = json.load(f)
    return {**DEFAULT_CONFIG, **user_cfg}

def save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)