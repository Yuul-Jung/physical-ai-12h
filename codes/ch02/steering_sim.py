"""02차시: 실제 장비 명령을 전송하지 않는 조향·후륜 구동 모의 실습."""
from dataclasses import dataclass
from math import radians, tan, sin, cos, isfinite
from typing import Iterable

@dataclass(frozen=True)
class VehicleSpec:
    wheelbase_m: float = 0.18  # 예시 모델 값; 실물 제원 아님
    max_steer_deg: float = 20.0  # 교육용 제한값; 알티노 AI 확정 사양 아님
    max_speed_mps: float = 0.35  # 모의 속도 제한
    max_accel_mps2: float = 0.4  # 모의 가감속 제한

@dataclass(frozen=True)
class Command:
    steer_deg: float
    speed_mps: float
    enabled: bool = False

@dataclass
class Pose:
    x_m: float = 0.0
    y_m: float = 0.0
    heading_rad: float = 0.0
    speed_mps: float = 0.0


def clamp(value: float, low: float, high: float) -> float:
    if low > high:
        raise ValueError('low must not exceed high')
    return max(low, min(high, value))


def sanitize(cmd: Command, spec: VehicleSpec) -> Command:
    """정지 조건을 우선하고 조향·속도 요청을 제한한다."""
    if not cmd.enabled:
        return Command(0.0, 0.0, False)
    # (변경) 비정상 명령값은 클램프하지 않고 안전 정지 요청으로 변환
    if not all(isfinite(v) for v in (cmd.steer_deg, cmd.speed_mps)):
        return Command(0.0, 0.0, False)
    if not all(isfinite(v) and v > 0 for v in (spec.max_steer_deg, spec.max_speed_mps, spec.max_accel_mps2)):
        raise ValueError('invalid vehicle specification')
    return Command(clamp(cmd.steer_deg, -spec.max_steer_deg, spec.max_steer_deg),
                   clamp(cmd.speed_mps, -spec.max_speed_mps, spec.max_speed_mps), True)


def update(pose: Pose, cmd: Command, dt_s: float, spec: VehicleSpec) -> Pose:
    """자전거 운동학 모델(교육용 근사): 실제 차량 동역학 아님."""
    if not isfinite(dt_s) or dt_s <= 0 or dt_s > 1:
        raise ValueError('dt_s must be finite and in (0, 1]')
    if not all(isfinite(v) for v in (pose.x_m, pose.y_m, pose.heading_rad, pose.speed_mps)):
        raise ValueError('pose contains nonfinite values')
    if not isfinite(spec.wheelbase_m) or spec.wheelbase_m <= 0:
        raise ValueError('wheelbase must be positive')
    safe = sanitize(cmd, spec)
    dv = clamp(safe.speed_mps - pose.speed_mps,
               -spec.max_accel_mps2 * dt_s, spec.max_accel_mps2 * dt_s)
    speed = pose.speed_mps + dv
    # 중점 적분: 회전하는 동안의 진행 방향을 반영한다.
    yaw_rate = speed * tan(radians(safe.steer_deg)) / spec.wheelbase_m
    mid_heading = pose.heading_rad + yaw_rate * dt_s / 2
    return Pose(pose.x_m + speed * cos(mid_heading) * dt_s,
                pose.y_m + speed * sin(mid_heading) * dt_s,
                pose.heading_rad + yaw_rate * dt_s, speed)


def simulate(commands: Iterable[Command], dt_s: float = 0.1,
             spec: VehicleSpec = VehicleSpec()) -> list[Pose]:
    poses = [Pose()]
    for command in commands:
        poses.append(update(poses[-1], command, dt_s, spec))
    return poses


def demo() -> None:
    spec = VehicleSpec()
    commands = ([Command(0, 0.25, True)] * 10 +
                [Command(15, 0.25, True)] * 10 +
                [Command(0, 0, False)] * 10)
    path = simulate(commands, 0.1, spec)
    print('step | x(m) | y(m) | heading(deg) | speed(m/s)')
    for i in (0, 10, 20, 30):
        p = path[i]
        print(f'{i:4d} | {p.x_m:5.3f} | {p.y_m:5.3f} | '
              f'{p.heading_rad * 180 / 3.141592653589793:12.2f} | {p.speed_mps:10.3f}')
    print('DRY RUN ONLY — no hardware commands were sent')


if __name__ == '__main__':
    demo()
