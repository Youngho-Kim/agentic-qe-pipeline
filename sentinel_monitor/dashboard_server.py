import os
import sys
import json
import time
import threading
import subprocess
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from config_manager import load_config, save_config
from probe_collector import check_endpoint
from noise_filter import TargetStateTracker
from notifier import AlertNotifier

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QA_STATUS_FILE = os.path.join(PARENT_DIR, "artifacts", "qa_pipeline_status.json")

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Sentinel-QE 통합 관제 & 자동 회귀 대시보드</title>
<style>
  body { font-family: 'Segoe UI', 'Pretendard', sans-serif; background: #0f1117; color: #e6edf3; margin: 0; padding: 24px; }
  .wrap { max-width: 1120px; margin: 0 auto; }
  .top { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 20px; }
  h1 { margin: 0; font-size: 22px; color: #58a6ff; }
  .btns { display: flex; gap: 8px; flex-wrap: wrap; }
  button { border: none; padding: 10px 15px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 13px; }
  .btn-primary { background: #238636; color: #fff; }
  .btn-auto { background: #1f6feb; color: #fff; }
  .btn-auto.active { background: #da3633; }
  .btn-demo { background: #8957e5; color: #fff; }
  .btn-qa { background: #d29922; color: #000; }
  .qa-banner { background: #161b22; border: 1px solid #30363d; border-left: 4px solid #3fb950; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(175px, 1fr)); gap: 14px; margin-bottom: 20px; }
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
  .alert-item.QA_TRIGGER { border-left-color: #d29922; }
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <h1>📡 Sentinel-QE 통합 관제 & 자동 회귀 대시보드</h1>
    <div class="btns">
      <button class="btn-primary" onclick="checkOnce()">🔄 1회 즉시 점검</button>
      <button class="btn-auto" id="btnAuto" onclick="toggleAuto()">▶️ 자동 감시 시작</button>
      <button class="btn-demo" onclick="runDemo()">🧪 오탐 필터링 시연</button>
      <button class="btn-qa" onclick="triggerQA()">🛡️ QA 정밀 재검증 (Step 3~4)</button>
    </div>
  </div>
  <div class="qa-banner" id="qaBanner">
    <div>
      <strong>🔗 최근 5단계 QA 릴리즈 연계 상태:</strong>
      <span id="qaSummary" style="margin-left:8px; color:#8b949e;">QA 실행 기록 대기 중 (Step 5 완료 시 자동 연동)</span>
    </div>
    <small id="qaUpdated" style="color:#8b949e;"></small>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="kpi-label">감시 대상 수</div><div class="kpi-val" id="kTotal">0</div></div>
    <div class="kpi"><div class="kpi-label">정상 (HEALTHY)</div><div class="kpi-val" style="color:#3fb950" id="kHealthy">0</div></div>
    <div class="kpi"><div class="kpi-label">장애 (CRITICAL)</div><div class="kpi-val" style="color:#f85149" id="kCrit">0</div></div>
    <div class="kpi"><div class="kpi-label">오탐 필터링 (차단)</div><div class="kpi-val" style="color:#d29922" id="kNoise">0</div></div>
    <div class="kpi"><div class="kpi-label">Slack / QA 자동 트리거</div><div class="kpi-val" style="color:#58a6ff" id="kAlerts">0</div></div>
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
    <h2>💬 Slack 경보 & Closed-Loop QA 자동 회귀 이력</h2>
    <div id="alertList" style="color:#8b949e; font-size:13px;">아직 발생한 경보가 없습니다.</div>
  </div>
</div>
<script>
async function refresh() {
  const res = await fetch('/api/state');
  const data = await res.json();
  if (data.qa_status) {
    document.getElementById('qaSummary').innerHTML =
      `<strong style="color:#e6edf3">${data.qa_status.decision}</strong> | 통과율: ${data.qa_status.pass_rate}% (${data.qa_status.passed}/${data.qa_status.total}건)`;
    document.getElementById('qaUpdated').innerText = '연동 시각: ' + data.qa_status.updated_at;
  }
  document.getElementById('kTotal').innerText = data.kpis.total_targets;
  document.getElementById('kHealthy').innerText = data.kpis.healthy;
  document.getElementById('kCrit').innerText = data.kpis.critical;
  document.getElementById('kNoise').innerText = data.kpis.filtered_noise;
  document.getElementById('kAlerts').innerText = data.kpis.total_alerts;
  const btnAuto = document.getElementById('btnAuto');
  btnAuto.innerText = data.auto_running ? '⏸️ 자동 감시 중지' : '▶️ 자동 감시 시작';
  btnAuto.classList.toggle('active', data.auto_running);
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
      </tr>`).join('');
  }
  const alertList = document.getElementById('alertList');
  if (data.alerts.length > 0) {
    alertList.innerHTML = data.alerts.map(a => `
      <div class="alert-item ${a.event}">
        <strong>${a.title}</strong> (${a.timestamp})<br>
        <span>대상: ${a.target} — ${a.message}</span>
      </div>`).join('');
  }
}
async function checkOnce() { await fetch('/api/check-once', {method:'POST'}); refresh(); }
async function toggleAuto() { await fetch('/api/toggle-auto', {method:'POST'}); refresh(); }
async function runDemo() { await fetch('/api/run-demo', {method:'POST'}); refresh(); }
async function triggerQA() { await fetch('/api/trigger-qa', {method:'POST'}); refresh(); }
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
</html>"""

class MonitorCoordinator:
    def __init__(self):
        self.cfg = load_config()
        self.lock = threading.Lock()
        self.tracker = TargetStateTracker(self.cfg["retry_threshold"], self.cfg["latency_warn_ms"])
        self.notifier = AlertNotifier(self.cfg["artifacts_dir"], self.cfg.get("slack_webhook_url", ""))
        self.urls = {}
        self.auto_running = False
        self.demo_running = False
        self.qa_running = False
        self.demo_cycle = 0

    def trigger_qa_regression(self, reason: str):
        if self.qa_running:
            return
        self.qa_running = True
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        step3_path = os.path.join(PARENT_DIR, "step3_test_runner.py")
        step4_path = os.path.join(PARENT_DIR, "step4_defect_triage.py")
        approved_xlsx = os.path.join(PARENT_DIR, "artifacts", "step2_approved_testcases.xlsx")

        with self.lock:
            self.notifier.alerts.insert(0, {
                "event": "QA_TRIGGER",
                "title": "🛡️ [Closed-Loop] QA 정밀 E2E 회귀 테스트 자동 출동",
                "target": reason,
                "message": "Step 3 (Playwright) & Step 4 (결함 트리아지) 자동 실행 중...",
                "timestamp": now
            })

        if os.path.exists(step3_path) and os.path.exists(approved_xlsx):
            try:
                subprocess.run([sys.executable, "step3_test_runner.py"], cwd=PARENT_DIR, check=False)
                if os.path.exists(step4_path):
                    subprocess.run([sys.executable, "step4_defect_triage.py"], cwd=PARENT_DIR, check=False)
                msg = "Playwright 정밀 재검증 및 RCA 트리아지 보고서 갱신 완료"
            except Exception as e:
                msg = f"QA 재검증 실행 중 오류: {str(e)[:50]}"
        else:
            msg = "승인된 QA 엑셀(step2_approved_testcases.xlsx)이 없어 시뮬레이션 트리거만 기록됨"

        with self.lock:
            self.notifier.alerts.insert(0, {
                "event": "QA_TRIGGER",
                "title": "✅ [Closed-Loop] QA 정밀 재검증 완료",
                "target": reason,
                "message": msg,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        self.qa_running = False

    def _handle_event(self, res: dict, state_obj: dict):
        if res["event"]:
            self.notifier.record_alert(res["event"], state_obj)
            if res["event"] == "CRITICAL_ALERT":
                threading.Thread(target=self.trigger_qa_regression, args=(res["target"],), daemon=True).start()

    def run_check_once(self):
        self.cfg = load_config()
        for t in self.cfg["targets"]:
            self.urls[t["name"]] = t["url"]
            ok, lat, detail = check_endpoint(t["url"], t.get("expected_status", 200), self.cfg.get("timeout_sec", 3))
            with self.lock:
                res = self.tracker.evaluate(t["name"], ok, lat, detail)
                state_obj = {**self.tracker.states[t["name"]], "name": t["name"], "message": res["message"]}
                self._handle_event(res, state_obj)
        with self.lock:
            self.notifier.write_markdown_report(self.tracker.states)

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
                self.urls[t["name"]] = t["url"]
                ok, lat, detail = check_endpoint(t["url"], 200, 2)
                with self.lock:
                    res = self.tracker.evaluate(t["name"], ok, lat, detail)
                    state_obj = {**self.tracker.states[t["name"]], "name": t["name"], "message": res["message"]}
                    self._handle_event(res, state_obj)
            with self.lock:
                self.notifier.write_markdown_report(self.tracker.states)
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
        qa_status = None
        if os.path.exists(QA_STATUS_FILE):
            try:
                with open(QA_STATUS_FILE, "r", encoding="utf-8") as f:
                    qa_status = json.load(f)
            except Exception:
                pass
        with self.lock:
            items = []
            for name, st in self.tracker.states.items():
                items.append({
                    "name": name,
                    "url": self.urls.get(name, ""),
                    "status": st["status"],
                    "last_latency_ms": st["last_latency_ms"],
                    "total_checks": st["total_checks"],
                    "total_failures": st["total_failures"],
                    "filtered_noise_count": st["filtered_noise_count"],
                    "message": st["last_detail"],
                    "last_checked": st["last_checked"]
                })
            return {
                "auto_running": self.auto_running,
                "demo_running": self.demo_running,
                "qa_status": qa_status,
                "kpis": {
                    "total_targets": len(items),
                    "healthy": sum(1 for i in items if i["status"] in ("HEALTHY", "RECOVERED")),
                    "critical": sum(1 for i in items if i["status"] == "CRITICAL"),
                    "filtered_noise": sum(i["filtered_noise_count"] for i in items),
                    "total_alerts": len(self.notifier.alerts)
                },
                "targets": items,
                "alerts": self.notifier.alerts
            }

coordinator = MonitorCoordinator()

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
            self._send_json(coordinator.get_snapshot())
        elif self.path == "/mock/healthy":
            self.send_response(200); self.end_headers(); self.wfile.write(b"OK")
        elif self.path == "/mock/flaky":
            self.send_response(503 if coordinator.demo_cycle == 2 else 200); self.end_headers(); self.wfile.write(b"Flaky")
        elif self.path == "/mock/outage":
            self.send_response(500 if coordinator.demo_cycle in (3, 4) else 200); self.end_headers(); self.wfile.write(b"Outage")
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path == "/api/check-once":
            threading.Thread(target=coordinator.run_check_once, daemon=True).start()
            self._send_json({"ok": True})
        elif self.path == "/api/toggle-auto":
            coordinator.auto_running = not coordinator.auto_running
            self._send_json({"auto_running": coordinator.auto_running})
        elif self.path == "/api/run-demo":
            threading.Thread(target=coordinator.run_demo_thread, daemon=True).start()
            self._send_json({"ok": True})
        elif self.path == "/api/trigger-qa":
            threading.Thread(target=coordinator.trigger_qa_regression, args=("수동 대시보드 요청",), daemon=True).start()
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

def start_dashboard():
    port = coordinator.cfg.get("port", 8900)
    threading.Thread(target=coordinator.auto_loop, daemon=True).start()
    return ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler), port