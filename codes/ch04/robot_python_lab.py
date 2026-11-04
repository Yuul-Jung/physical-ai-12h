"""04차시: 로봇 명령을 생성하는 Python 기초. 실제 모터를 구동하지 않는다."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Command:
    steering_deg: float
    speed_pct: float
    reason: str

def clamp(value: float, low: float, high: float) -> float:
    """안전한 출력 범위로 제한한다."""
    if not isfinite(value):
        raise ValueError('값은 유한한 수여야 합니다')
    if low > high:
        raise ValueError('범위의 최소값이 최대값보다 큽니다')
    return min(max(value, low), high)

def decide(front_m: float | None, target_direction: str) -> Command:
    """거리와 목표 방향으로 모의 주행 명령을 만든다."""
    if front_m is None or not isfinite(front_m) or front_m < 0:
        return Command(0.0, 0.0, '거리 측정 오류: 정지')
    if front_m < 0.5:
        return Command(0.0, 0.0, '전방 장애물: 정지')
    direction_to_angle = {'left': -15.0, 'straight': 0.0, 'right': 15.0}
    if target_direction not in direction_to_angle:
        return Command(0.0, 0.0, '알 수 없는 방향: 정지')
    speed = 20.0 if front_m < 1.0 else 35.0
    return Command(direction_to_angle[target_direction], speed, '모의 명령')

def run_scenario(measurements: list[float | None], direction: str) -> list[Command]:
    """반복문으로 센서 샘플을 순서대로 처리한다."""
    return [decide(distance, direction) for distance in measurements]

def main() -> None:
    distances = [1.8, 0.8, 0.3, None]
    for index, command in enumerate(run_scenario(distances, 'left'), start=1):
        print(f'{index}: 조향={command.steering_deg:.0f}도 속도={command.speed_pct:.0f}% / {command.reason}')

if __name__ == '__main__':
    main()
