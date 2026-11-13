import os
import json
from datetime import datetime
from typing import Dict, Any

class AlertNotifier:
    def __init__(self, artifacts_dir: str, webhook_url: str = ""):
        self.artifacts_dir = artifacts_dir
        self.webhook_url = webhook_url.strip()
        os.makedirs(self.artifacts_dir, exist_ok=True)
        self.alert_log_path = os.path.join(self.artifacts_dir, "slack_alerts_history.json")
        self.report_path = os.path.join(self.artifacts_dir, "monitoring_status_report.md")
        self.alerts = []

    def record_alert(self, event: str, state: Dict[str, Any]) -> Dict[str, Any]:
        import urllib.request
        is_crit = (event == "CRITICAL_ALERT")
        title = "🚨 [장애 경보] 서비스 응답 불가 확정" if is_crit else "✅ [복구 완료] 서비스 정상화"
        entry = {
            "event": event,
            "title": title,
            "target": state["name"],
            "message": state["message"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.alerts.insert(0, entry)
        self.alerts = self.alerts[:30]
        with open(self.alert_log_path, "w", encoding="utf-8") as f:
            json.dump(self.alerts, f, indent=2, ensure_ascii=False)

        if self.webhook_url:
            try:
                payload = {"text": f"{title}\n*대상*: {state['name']}\n*내용*: {state['message']}"}
                req = urllib.request.Request(
                    self.webhook_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                urllib.request.urlopen(req, timeout=4)
            except Exception:
                pass
        return entry

    def write_markdown_report(self, states: Dict[str, Dict[str, Any]]):
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("# 📡 Sentinel 서비스 헬스체크 보고서\n\n")
            f.write(f"- **갱신 시각**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| 서비스명 | 상태 | 점검 | 실패 | 오탐 필터링 | 응답속도 | 비고 |\n")
            f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |\n")
            for name, st in states.items():
                f.write(f"| {name} | {st['status']} | {st['total_checks']} | {st['total_failures']} | {st['filtered_noise_count']} | {st['last_latency_ms']}ms | {st['last_detail']} |\n")