import threading
import webbrowser
from dashboard_server import start_dashboard

def main():
    server, port = start_dashboard()
    url = f"http://127.0.0.1:{port}"
    print("=" * 60)
    print(f"📡 [Sentinel-QE Modular Dashboard] 실행 중: {url}")
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