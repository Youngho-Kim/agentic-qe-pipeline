import os
import sys
import subprocess

def main():
    while True:
        print("\n" + "=" * 65)
        print("🛡️ [All-in-One QE Platform] 배포 전 QA & 배포 후 모니터링 통합 런처")
        print("=" * 65)
        print("  1. [Pre-Release]  5단계 AI-QE 파이프라인 + 엑셀 DDT 실행")
        print("  2. [Post-Release] 실시간 서비스 헬스체크 대시보드 실행 (Sentinel)")
        print("  3. [Domain Demo]  팬딩(Fanding) 멤버십/결제 특화 테스트 실행")
        print("  4. [Mobile Demo]  티피씨(LIKEY) iPhone 14 모바일 테스트 실행")
        print("  0. 종료")
        print("=" * 65)

        choice = input("👉 실행할 번호를 선택하세요 (1~4, 종료=0): ").strip()

        if choice == "1":
            subprocess.run([sys.executable, "run_modular_qe_pipeline.py"])
        elif choice == "2":
            monitor_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sentinel_monitor")
            if not os.path.exists(os.path.join(monitor_dir, "sentinel_app.py")):
                print("❌ 'sentinel_monitor/sentinel_app.py' 폴더를 찾을 수 없습니다.")
            else:
                subprocess.run([sys.executable, "sentinel_app.py"], cwd=monitor_dir)
        elif choice == "3":
            if os.path.exists("run_fanding_membership_qa.py"):
                subprocess.run([sys.executable, "run_fanding_membership_qa.py"])
            else:
                print("❌ 'run_fanding_membership_qa.py' 파일이 없습니다.")
        elif choice == "4":
            if os.path.exists("run_likey_mobile_qa.py"):
                subprocess.run([sys.executable, "run_likey_mobile_qa.py"])
            else:
                print("❌ 'run_likey_mobile_qa.py' 파일이 없습니다.")
        elif choice == "0":
            print("👋 통합 런처를 종료합니다.")
            break
        else:
            print("⚠️ 0~4 사이의 번호를 입력해 주세요.")

if __name__ == "__main__":
    main()