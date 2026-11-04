"""1차시: 로봇과 PC 공통으로 실행 가능한 읽기 전용 환경 점검."""
import json
import os
import platform
import sys
from pathlib import Path


def collect_environment():
    """계정명·호스트명·IP·일련번호를 수집하지 않는다."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "os_family": platform.system(),
        "architecture": platform.machine(),
        "virtual_environment": sys.prefix != sys.base_prefix,
        "working_directory_accessible": Path.cwd().is_dir(),
        "display_configured": bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    }


def main():
    print(json.dumps(collect_environment(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
