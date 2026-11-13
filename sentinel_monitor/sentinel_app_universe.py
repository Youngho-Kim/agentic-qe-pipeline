import os
import json
import time
import threading
import webbrowser
import urllib.request
import urllib.error
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

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

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

class SentinelEngine:
    def __init__(self):
        self.cfg = load_config()
        self.lock = threading.Lock()
        self.states = {}
        self.alerts = []
        self.auto_running = False
        self.demo_running = False
        self.demo_cycle = 0
        os.makedirs(self.cfg["artifacts_dir"], exist_ok=True)
        self.alert_log_path = os.path.join(self.cfg["artifacts_dir"], "slack_alerts_history.json")
        self.report_path = os.path.join(self.cfg["artifacts_dir"], "monitoring_status_report.md")

    def check_url(self, url: str, expected_status: int, timeout_sec: int):
        start_t = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Sentinel-QE-Dashboard/1.0"})
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                code = resp.getcode()
                latency_ms = (time.time() - start_t) * 1000
                if code == expected_status:
                    return True, latency_ms, f"HTTP {code} OK"
                return False, latency_ms, f"HTTP {code} (기대: {expected_status})"
        except urllib.error.HTTPError as e:
            return False, (time.time() - start_t) * 1000, f"HTTP Error {e.code}"
        except Exception as e:
            return False, (time.time() - start_t) * 1000, str(e)[:60]

    def evaluate(self, target_name: str, url: str, ok: bool, latency_ms: float, detail: str):
        now = datetime.now().strftime("%H:%M:%S")
        retry_threshold = self.cfg.get("retry_threshold", 2)
        latency_warn = self.cfg.get("latency_warn_ms", 800)

        with self.lock:
            prev = self.states.get(target_name, {
                "name": target_name,
                "url": url,
                "status": "HEALTHY",
                "consecutive_failures": 0,
                "total_checks": 0,
                "total_failures": 0,
                "filtered_noise_count": 0,
                "last_latency_ms": 0.0,
                "last_checked": now,
                "message": "대기 중"
            })
            prev["url"] = url
            prev["total_checks"] += 1
            prev["last_checked"] = now
            prev["last_latency_ms"] = round(latency_ms, 1)

            event = None
            if ok:
                if prev["status"] == "SUSPECT":
                    prev["filtered_noise_count"] += 1
                    prev["status"] = "HEALTHY"
                    prev["consecutive_failures"] = 0
                    prev["message"] = "일시적 순단 후 복구 (오탐 필터링됨)"
                elif prev["status"] == "CRITICAL":
                    prev["status"] = "RECOVERED"
                    prev["consecutive_failures"] = 0
                    event = "RECOVERED_ALERT"
                    prev["message"] = "장애 상태에서 정상 복구됨"
                else:
                    prev["status"] = "HEALTHY"
                    prev["consecutive_failures"] = 0
                    prev["message"] = f"응답 지연 주의 ({latency_ms:.0f}ms)" if latency_ms > latency_warn else "정상 응답"
            else:
                prev["total_failures"] += 1
                prev["consecutive_failures"] += 1
                if prev["consecutive_failures"] < retry_threshold:
                    prev["status"] = "SUSPECT"
                    prev["message"] = f"1차 이상 감지 ({prev['consecutive_failures']}/{retry_threshold}) - 재확인 대기"
                else:
                    if prev["status"] != "CRITICAL":
                        event = "CRITICAL_ALERT"
                    prev["status"] = "CRITICAL"
                    prev["message"] = f"연속 {prev['consecutive_failures']}회 실패 - 장애 확정 ({detail})"

            self.states[target_name] = prev

        if event:
            self.record_alert(event, prev)

    def record_alert(self, event: str, state: dict):
        is_crit = (event == "CRITICAL_ALERT")
        title = "🚨 [장애 경보] 서비스 응답 불가 확정" if is_crit else "✅ [복구 완료] 서비스 정상화"
        alert_entry = {
            "event": event,
            "title": title,
            "target": state["name"],
            "message": state["message"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with self.lock:
            self.alerts.insert(0, alert_entry)
            self.alerts = self.alerts[:30]
            with open(self.alert_log_path, "w", encoding="utf-8") as f:
                json.dump(self.alerts, f, indent=2, ensure_ascii=False)

        webhook = self.cfg.get("slack_webhook_url", "").strip()
        if webhook:
            try:
                payload = {"text": f"{title}\n*대상*: {state['name']}\n*내용*: {state['message']}"}
                req = urllib.request.Request(webhook, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=4)
            except Exception:
                pass

    def write_markdown_report(self):
        with self.lock:
            states_copy = dict(self.states)
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("# 📡 Sentinel 서비스 헬스체크 보고서\n\n")
            f.write(f"- **갱신 시각**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| 서비스명 | 상태 | 점검 | 실패 | 오탐 필터링 | 응답속도 | 비고 |\n")
            f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |\n")
            for st in states_copy.values():
                f.write(f"| {st['name']} | {st['status']} | {st['total_checks']} | {st['total_failures']} | {st['filtered_noise_count']} | {st['last_latency_ms']}ms | {st['message']} |\n")

    def run_check_once(self):
        self.cfg = load_config()
        for t in self.cfg["targets"]:
            ok, lat, detail = self.check_url(t["url"], t.get("expected_status", 200), self.cfg.get("timeout_sec", 3))
            self.evaluate(t["name"], t["url"], ok, lat, detail)
        self.write_markdown_report()

    def run_demo_thread(self):
        if self.demo_running:
            return
        self.demo_running = True
        port = self.cfg.get("port", 8900)
        demo_targets = [
            {"name": "[Demo] Auth API (정상)", "url": f"http://127.0.0.1:{port}/mock/healthy"},
            {"name": "[Demo] Search API (단발순단)", "url": f"http://127.0.0.1:{port}/mock/flaky"},
            {"name": "[Demo] Payment API (실제장애)", "url": f"http://127.0.0.1:{port}/mock/outage"}
        ]
        for cycle in range(1, 6):
            self.demo_cycle = cycle
            for t in demo_targets:
                ok, lat, detail = self.check_url(t["url"], 200, 2)
                self.evaluate(t["name"], t["url"], ok, lat, detail)
            self.write_markdown_report()
            time.sleep(1.0)
        self.demo_running = False

    def auto_loop(self):
        while True:
            if self.auto_running:
                self.run_check_once()
                time.sleep(self.cfg.get("check_interval_sec", 5))
            else:
                time.sleep(0.5)

    def get_snapshot(self):
        with self.lock:
            items = list(self.states.values())
            return {
                "auto_running": self.auto_running,
                "demo_running": self.demo_running,
                "kpis": {
                    "total_targets": len(items),
                    "healthy": sum(1 for i in items if i["status"] in ("HEALTHY", "RECOVERED")),
                    "critical": sum(1 for i in items if i["status"] == "CRITICAL"),
                    "filtered_noise": sum(i["filtered_noise_count"] for i in items),
                    "total_alerts": len(self.alerts)
                },
                "targets": items,
                "alerts": self.alerts
            }

engine = SentinelEngine()

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Sentinel-QE 서비스 헬스체크 대시보드</title>
<style>
  body { font-family: 'Segoe UI', 'Pretendard', sans-serif; background: #0f1117; color: #e6edf3; margin: 0; padding: 24px; }
  .wrap { max-width: 1100px; margin: 0 auto; }
  .top { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 24px; }
  h1 { margin: 0; font-size: 22px; color: #58a6ff; }
  .btns { display: flex; gap: 8px; flex-wrap: wrap; }
  button { border: none; padding: 10px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 13px; }
  .btn-primary { background: #238636; color: #fff; }
  .btn-auto { background: #1f6feb; color: #fff; }
  .btn-auto.active { background: #da3633; }
  .btn-demo { background: #8957e5; color: #fff; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 24px; }
  .kpi { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 16px; }
  .kpi-label { font-size: 12px; color: #8b949e; margin-bottom: 6px; }
  .kpi-val { font-size: 26px; font-weight: 700; }
  .panel { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 18px; margin-bottom: 20px; }
  .panel h2 { margin: 0 0 14px 0; font-size: 16px; color: #c9d1d9; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid #21262d; }
  th { color: #8b949e; font-weight: 600; }
  .badge { padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; display: inline-block; }
  .HEALTHY, .RECOVERED { background: rgba(46,160,67,0.2); color: #3fb950; }
  .SUSPECT { background: rgba(210,153,34,0.2); color: #d29922; }
  .CRITICAL { background: rgba(248,81,73,0.2); color: #f85149; }
  .add-form { display: flex; gap: 8px; flex-wrap: wrap; }
  input { background: #0d1117; border: 1px solid #30363d; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 13px; }
  .alert-item { padding: 10px; border-left: 3px solid #f85149; background: #0d1117; margin-bottom: 8px; border-radius: 4px; font-size: 13px; }
  .alert-item.RECOVERED_ALERT { border-left-color: #3fb950; }
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <h1>📡 Sentinel-QE 서비스 헬스체크 대시보드</h1>
    <div class="btns">
      <button class="btn-primary" onclick="checkOnce()">🔄 1회 즉시 점검</button>
      <button class="btn-auto" id="btnAuto" onclick="toggleAuto()">▶️ 자동 감시 시작</button>
      <button class="btn-demo" onclick="runDemo()">🧪 오탐 필터링 시연 (5초)</button>
    </div>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="kpi-label">감시 대상 수</div><div class="kpi-val" id="kTotal">0</div></div>
    <div class="kpi"><div class="kpi-label">정상 (HEALTHY)</div><div class="kpi-val" style="color:#3fb950" id="kHealthy">0</div></div>
    <div class="kpi"><div class="kpi-label">장애 (CRITICAL)</div><div class="kpi-val" style="color:#f85149" id="kCrit">0</div></div>
    <div class="kpi"><div class="kpi-label">오탐 필터링 (차단)</div><div class="kpi-val" style="color:#d29922" id="kNoise">0</div></div>
    <div class="kpi"><div class="kpi-label">Slack 경보 발행</div><div class="kpi-val" style="color:#58a6ff" id="kAlerts">0</div></div>
  </div>

  <div class="panel">
    <h2>🎯 실시간 모니터링 대상 현황</h2>
    <table>
      <thead><tr><th>서비스명</th><th>상태</th><th>응답속도</th><th>점검 / 실패</th><th>오탐 차단</th><th>상세 메시지</th><th>최근 점검</th></tr></thead>
      <tbody id="targetBody"><tr><td colspan="7" style="color:#8b949e; text-align:center;">상단의 [1회 즉시 점검] 또는 [오탐 필터링 시연] 버튼을 눌러주세요.</td></tr></tbody>
    </table>
  </div>

  <div class="panel">
    <h2>➕ 감시 URL 추가</h2>
    <div class="add-form">
      <input type="text" id="newName" placeholder="서비스 이름 (예: 팬딩 메인)">
      <input type="text" id="newUrl" placeholder="https://example.com" style="flex:1; min-width:240px;">
      <button class="btn-primary" onclick="addTarget()">추가 후 저장</button>
    </div>
  </div>

  <div class="panel">
    <h2>💬 Slack 경보 및 복구 알림 이력</h2>
    <div id="alertList" style="color:#8b949e; font-size:13px;">아직 발생한 경보가 없습니다.</div>
  </div>
</div>

<script>
async function refresh() {
  const res = await fetch('/api/state');
  const data = await res.json();
  document.getElementById('kTotal').innerText = data.kpis.total_targets;
  document.getElementById('kHealthy').innerText = data.kpis.healthy;
  document.getElementById('kCrit').innerText = data.kpis.critical;
  document.getElementById('kNoise').innerText = data.kpis.filtered_noise;
  document.getElementById('kAlerts').innerText = data.kpis.total_alerts;

  const btnAuto = document.getElementById('btnAuto');
  if (data.auto_running) {
    btnAuto.innerText = '⏸️ 자동 감시 중지';
    btnAuto.classList.add('active');
  } else {
    btnAuto.innerText = '▶️ 자동 감시 시작';
    btnAuto.classList.remove('active');
  }

  const tbody = document.getElementById('targetBody');
  if (data.targets.length > 0) {
    tbody.innerHTML = data.targets.map(t => `
      <tr>
        <td><strong>${t.name}</strong><br><small style="color:#8b949e">${t.url}</small></td>
        <td><span class="badge ${t.status}">${t.status}</span></td>
        <td>${t.last_latency_ms} ms</td>
        <td>${t.total_checks} / ${t.total_failures}</td>
        <td>${t.filtered_noise_count} 건</td>
        <td>${t.message}</td>
        <td>${t.last_checked}</td>
      </tr>
    `).join('');
  }

  const alertList = document.getElementById('alertList');
  if (data.alerts.length > 0) {
    alertList.innerHTML = data.alerts.map(a => `
      <div class="alert-item ${a.event}">
        <strong>${a.title}</strong> (${a.timestamp})<br>
        <span>대상: ${a.target} — ${a.message}</span>
      </div>
    `).join('');
  }
}

async function checkOnce() { await fetch('/api/check-once', {method:'POST'}); refresh(); }
async function toggleAuto() { await fetch('/api/toggle-auto', {method:'POST'}); refresh(); }
async function runDemo() { await fetch('/api/run-demo', {method:'POST'}); refresh(); }
async function addTarget() {
  const name = document.getElementById('newName').value.trim();
  const url = document.getElementById('newUrl').value.trim();
  if (!name || !url) return alert('이름과 URL을 모두 입력해 주세요.');
  await fetch('/api/add-target', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name, url})});
  document.getElementById('newName').value = '';
  document.getElementById('newUrl').value = '';
  checkOnce();
}

setInterval(refresh, 1000);
refresh();
</script>
</body>
</html>
"""

class DashboardHandler(BaseHTTPRequestHandler):
    def _send_json(self, obj, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
        elif self.path == "/api/state":
            self._send_json(engine.get_snapshot())
        elif self.path == "/mock/healthy":
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
        elif self.path == "/mock/flaky":
            code = 503 if engine.demo_cycle == 2 else 200
            self.send_response(code); self.end_headers(); self.wfile.write(b"Flaky")
        elif self.path == "/mock/outage":
            code = 500 if engine.demo_cycle in (3, 4) else 200
            self.send_response(code); self.end_headers(); self.wfile.write(b"Outage")
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path == "/api/check-once":
            threading.Thread(target=engine.run_check_once, daemon=True).start()
            self._send_json({"ok": True})
        elif self.path == "/api/toggle-auto":
            engine.auto_running = not engine.auto_running
            self._send_json({"auto_running": engine.auto_running})
        elif self.path == "/api/run-demo":
            threading.Thread(target=engine.run_demo_thread, daemon=True).start()
            self._send_json({"ok": True})
        elif self.path == "/api/add-target":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            cfg = load_config()
            cfg["targets"].append({"name": body["name"], "url": body["url"], "expected_status": 200})
            save_config(cfg)
            self._send_json({"ok": True})
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, format, *args):
        pass

def main():
    port = engine.cfg.get("port", 8900)
    threading.Thread(target=engine.auto_loop, daemon=True).start()
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler)
    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print(f"📡 [Sentinel-QE Dashboard] 실행 중: {url}")
    print("👉 브라우저가 자동으로 열립니다. (종료: Ctrl+C)")
    print("=" * 60)
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 모니터링 대시보드를 종료했습니다.")
        server.shutdown()

if __name__ == "__main__":
    main()