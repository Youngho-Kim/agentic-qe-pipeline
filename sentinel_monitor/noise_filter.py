from datetime import datetime
from typing import Dict, Any

class TargetStateTracker:
    def __init__(self, retry_threshold: int = 2, latency_warn_ms: int = 800):
        self.retry_threshold = retry_threshold
        self.latency_warn_ms = latency_warn_ms
        self.states: Dict[str, Dict[str, Any]] = {}

    def evaluate(self, target_name: str, ok: bool, latency_ms: float, detail: str) -> Dict[str, Any]:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prev = self.states.get(target_name, {
            "status": "HEALTHY",
            "consecutive_failures": 0,
            "total_checks": 0,
            "total_failures": 0,
            "filtered_noise_count": 0,
            "last_latency_ms": 0.0,
            "last_checked": now,
            "last_detail": "초기화"
        })

        prev["total_checks"] += 1
        prev["last_checked"] = now
        prev["last_latency_ms"] = round(latency_ms, 1)
        prev["last_detail"] = detail

        event = None

        if ok:
            if prev["status"] == "SUSPECT":
                prev["filtered_noise_count"] += 1
                prev["status"] = "HEALTHY"
                prev["consecutive_failures"] = 0
                detail_msg = "일시적 순단 후 정상 복구 (오탐 필터링됨)"
            elif prev["status"] == "CRITICAL":
                prev["status"] = "RECOVERED"
                prev["consecutive_failures"] = 0
                event = "RECOVERED_ALERT"
                detail_msg = "장애 상태에서 정상 서비스로 복구됨"
            else:
                prev["status"] = "HEALTHY"
                prev["consecutive_failures"] = 0
                detail_msg = "정상 응답"
                if latency_ms > self.latency_warn_ms:
                    detail_msg = f"응답 지연 주의 ({latency_ms:.0f}ms)"
        else:
            prev["total_failures"] += 1
            prev["consecutive_failures"] += 1

            if prev["consecutive_failures"] < self.retry_threshold:
                prev["status"] = "SUSPECT"
                detail_msg = f"1차 이상 감지 ({prev['consecutive_failures']}/{self.retry_threshold}) - 오탐 여부 재확인 대기"
            else:
                if prev["status"] != "CRITICAL":
                    event = "CRITICAL_ALERT"
                prev["status"] = "CRITICAL"
                detail_msg = f"연속 {prev['consecutive_failures']}회 실패 - 실제 장애 확정 ({detail})"

        self.states[target_name] = prev
        return {
            "target": target_name,
            "status": prev["status"],
            "event": event,
            "latency_ms": prev["last_latency_ms"],
            "consecutive_failures": prev["consecutive_failures"],
            "filtered_noise_count": prev["filtered_noise_count"],
            "message": detail_msg,
            "timestamp": now
        }