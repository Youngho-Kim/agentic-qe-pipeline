import time
import urllib.request
import urllib.error
from typing import Tuple

def check_endpoint(url: str, expected_status: int = 200, timeout_sec: int = 3) -> Tuple[bool, float, str]:
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