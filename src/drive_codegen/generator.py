"""Jinja2 模板渲染与文件输出."""

from __future__ import annotations

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import DriveConfig

TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "templates"


def load_config(path: Path) -> DriveConfig:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return DriveConfig.from_dict(data)


def render_all(config: DriveConfig, output_dir: Path) -> list[Path]:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(disabled_extensions=("j2",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    ctx = {
        "cfg": config.raw,
        "shunt": config.shunt,
        "project_name": config.get("project", "name", default="drive"),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for template_name, out_name in (
        ("current_sense.h.j2", "current_sense.h"),
        ("motor_pwm.c.j2", "motor_pwm.c"),
        ("drive_config.h.j2", "drive_config.h"),
    ):
        text = env.get_template(template_name).render(**ctx)
        out_path = output_dir / out_name
        out_path.write_text(text, encoding="utf-8")
        written.append(out_path)

    return written
