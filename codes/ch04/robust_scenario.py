"""04차시 선택 실습: 안전한 거리 데이터 입력, 판정, CSV 기록(모의 명령)."""
from pathlib import Path
from csv import DictWriter
from math import isfinite
from robot_python_lab import decide


def parse_distance(raw):
    """센서 문자열을 미터 값으로 변환; 비정상 값은 None으로 정규화한다."""
    try:
        number = float(raw)
    except (ValueError, TypeError):
        return None
    return number if isfinite(number) and number >= 0 else None


def make_log(rows, direction='straight'):
    """센서 입력→예외 처리→명령 생성→감사 가능한 기록을 만든다."""
    output = []
    for index, value in enumerate(rows, 1):
        distance = parse_distance(value)
        cmd = decide(distance, direction)
        output.append({'sequence': index, 'raw': str(value),
                       'distance_m': '' if distance is None else distance,
                       'steering_deg': cmd.steering_deg,
                       'speed_pct': cmd.speed_pct,
                       'reason': cmd.reason})
    return output


def save_csv(output, path):
    """외부 장비에 명령을 보내지 않고 로컬 CSV 파일만 저장한다."""
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('w', encoding='utf-8-sig', newline='') as f:
        writer = DictWriter(f, fieldnames=['sequence', 'raw', 'distance_m',
                                         'steering_deg', 'speed_pct', 'reason'])
        writer.writeheader()
        writer.writerows(output)
    return dest


if __name__ == '__main__':
    readings = ['1.8', '0.8', 'bad', '-1', 'nan', '0.3', '2.0']
    log = make_log(readings, 'left')
    for row in log:
        print(f"{row['sequence']}: {row['raw']:>5} → 속도 {row['speed_pct']:.0f}% / {row['reason']}")
    print('CSV 저장:', save_csv(log, Path(__file__).parent / 'output' / 'decisions.csv'))
