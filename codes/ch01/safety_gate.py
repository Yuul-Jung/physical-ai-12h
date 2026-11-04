"""1차시: 물리 구동 없이 안전 조건을 판단하는 순수 Python 예제."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyInputs:
    emergency_stop_released: bool
    wheels_clear: bool
    operator_present: bool
    power_ok: bool
    software_ready: bool


def may_enable_motion(state: SafetyInputs) -> bool:
    """모든 안전 조건이 충족될 때만 True를 반환한다."""
    return all((state.emergency_stop_released, state.wheels_clear,
                state.operator_present, state.power_ok, state.software_ready))


def main():
    safe = SafetyInputs(True, True, True, True, True)
    blocked = SafetyInputs(True, False, True, True, True)
    print("모든 조건 충족:", may_enable_motion(safe))
    print("차륜 안전 미확인:", may_enable_motion(blocked))


if __name__ == "__main__":
    main()
