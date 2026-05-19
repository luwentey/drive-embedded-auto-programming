"""命令行入口."""

from __future__ import annotations

import argparse
from pathlib import Path

from .generator import load_config, render_all


def main() -> None:
    parser = argparse.ArgumentParser(
        description="驱动器嵌入式软件自动编程 — 从 YAML 生成 C 代码",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="根据配置文件生成代码")
    gen.add_argument("-c", "--config", type=Path, required=True, help="YAML 配置路径")
    gen.add_argument("-o", "--output", type=Path, default=Path("output"), help="输出目录")

    calc = sub.add_parser("calc-shunt", help="计算采样电阻阻值与功耗")
    calc.add_argument("--max-current", type=float, required=True, help="最大电流 (A)")
    calc.add_argument(
        "--target-mv",
        type=float,
        default=100.0,
        help="满量程采样电压 (mV)",
    )

    args = parser.parse_args()

    if args.command == "generate":
        cfg = load_config(args.config)
        paths = render_all(cfg, args.output)
        print(f"已生成 {len(paths)} 个文件 -> {args.output.resolve()}")
        for p in paths:
            print(f"  {p.name}")
        s = cfg.shunt
        print(
            f"采样电阻: {s.resistance_mohm:.3f} mΩ, "
            f"建议功率 >= {s.power_w:.2f} W"
        )
    elif args.command == "calc-shunt":
        from .models import calc_shunt

        s = calc_shunt(args.max_current, args.target_mv)
        print(f"Rshunt = {s.resistance_mohm:.3f} mΩ ({s.resistance_ohm:.6f} Ω)")
        print(f"建议功率 (2x 余量) >= {s.power_w:.2f} W")
        print(f"满量程采样电压 = {s.sense_voltage_v * 1000:.1f} mV @ {s.max_current_a} A")


if __name__ == "__main__":
    main()
