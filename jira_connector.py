import os
import json
import base64
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional

REGISTRY_FILE = os.path.join("artifacts", "jira_registered_issues.json")

def _load_local_registry() -> dict:
    if not os.path.exists(REGISTRY_FILE):
        return {}
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_local_registry(reg: dict):
    os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)

def find_open_jira_issue(base_url: str, auth_str: str, project_key: str, tc_id: str) -> Optional[str]:
    jql = f'project = "{project_key}" AND summary ~ "{tc_id}" AND statusCategory != Done'
    query = urllib.parse.urlencode({"jql": jql, "maxResults": 1, "fields": "key,summary,status"})
    req = urllib.request.Request(
        f"{base_url}/rest/api/2/search?{query}",
        headers={"Authorization": f"Basic {auth_str}", "Accept": "application/json"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            issues = data.get("issues", [])
            if issues:
                return issues[0].get("key")
    except Exception:
        pass
    return None

def create_jira_issue(jira_cfg: Dict[str, Any], defect: Dict[str, Any]) -> Dict[str, Any]:
    base_url = jira_cfg.get("base_url", "").rstrip("/")
    email = jira_cfg.get("email", "").strip()
    api_token = jira_cfg.get("api_token", "").strip()
    project_key = jira_cfg.get("project_key", "KAN").strip()
    tc_id = defect["tc_id"]

    # 1. 로컬 중복 이력 확인
    registry = _load_local_registry()
    if tc_id in registry:
        return {
            "mode": "deduplicated",
            "created": False,
            "skipped": True,
            "existing_key": registry[tc_id].get("issue_key"),
            "reason": f"이미 등록된 결함({registry[tc_id].get('issue_key')})이므로 중복 등록을 건너뛰었습니다."
        }

    description = (
        f"[결함 분류] {defect['classification']}\n"
        f"[심각도] {defect['severity']}\n"
        f"[재현 스텝] {defect.get('failed_step')}\n"
        f"[원시 에러] {defect['error_msg']}\n"
        f"[증빙 캡처] {defect['screenshot']}\n"
        f"[권장 조치] {defect['action']}"
    )

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": f"[{defect['severity']}] {tc_id}: {defect['title']}",
            "description": description,
            "issuetype": {"name": jira_cfg.get("issue_type", "Bug")}
        }
    }

    if not (base_url and email and api_token):
        return {"mode": "simulation", "created": False, "payload": payload}

    auth_str = base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")

    # 2. Jira 서버 실시간 JQL 중복 확인
    existing_key = find_open_jira_issue(base_url, auth_str, project_key, tc_id)
    if existing_key:
        registry[tc_id] = {"issue_key": existing_key, "url": f"{base_url}/browse/{existing_key}"}
        _save_local_registry(registry)
        return {
            "mode": "live_deduplicated",
            "created": False,
            "skipped": True,
            "existing_key": existing_key,
            "reason": f"Jira에 미결 이슈({existing_key})가 이미 열려 있어 중복 등록을 방지했습니다."
        }

    # 3. 신규 버그 티켓 생성
    req = urllib.request.Request(
        f"{base_url}/rest/api/2/issue",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Basic {auth_str}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            key = res_data.get("key")
            url = f"{base_url}/browse/{key}"
            registry[tc_id] = {"issue_key": key, "url": url}
            _save_local_registry(registry)
            return {"mode": "live", "created": True, "issue_key": key, "url": url}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return {"mode": "live", "created": False, "error": f"HTTP {e.code}: {err_body[:150]}"}
    except Exception as e:
        return {"mode": "live", "created": False, "error": str(e)}