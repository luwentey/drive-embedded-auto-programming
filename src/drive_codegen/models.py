"""驱动器配置数据模型与采样电阻计算."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ShuntSpec:
    resistance_ohm: float
    power_w: float
    sense_voltage_v: float
    max_current_a: float

    @property
    def resistance_mohm(self) -> float:
        return self.resistance_ohm * 1000.0


def calc_shunt(
    max_current_a: float,
    target_sense_voltage_mv: float,
    *,
    power_margin: float = 2.0,
) -> ShuntSpec:
    """根据最大电流与目标采样电压计算 shunt 阻值与建议功率."""
    sense_v = target_sense_voltage_mv / 1000.0
    if max_current_a <= 0:
        raise ValueError("max_current_a 必须大于 0")
    r = sense_v / max_current_a
    p = max_current_a**2 * r
    return ShuntSpec(
        resistance_ohm=r,
        power_w=p * power_margin,
        sense_voltage_v=sense_v,
        max_current_a=max_current_a,
    )


@dataclass
class DriveConfig:
    raw: dict[str, Any]
    shunt: ShuntSpec = field(repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DriveConfig:
        motor = data.get("motor", {})
        sampling = data.get("sampling", {})
        shunt_cfg = sampling.get("shunt", {})
        max_i = float(motor.get("max_current_a", 10.0))
        target_mv = float(shunt_cfg.get("target_sense_voltage_mv", 100))

        if "resistance_mohm" in shunt_cfg:
            r = float(shunt_cfg["resistance_mohm"]) / 1000.0
            sense_v = target_mv / 1000.0
            p = float(shunt_cfg.get("power_w", max_i**2 * r * 2.0))
            shunt = ShuntSpec(
                resistance_ohm=r,
                power_w=p,
                sense_voltage_v=sense_v,
                max_current_a=max_i,
            )
        else:
            shunt = calc_shunt(max_i, target_mv)

        return cls(raw=data, shunt=shunt)

    def get(self, *keys: str, default: Any = None) -> Any:
        node: Any = self.raw
        for k in keys:
            if not isinstance(node, dict):
                return default
            node = node.get(k, default)
            if node is default and k != keys[-1]:
                return default
        return node
