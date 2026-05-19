# 驱动器嵌入式软件自动编程 (Drive Embedded Auto-Programming)

面向电机/变频器驱动器的嵌入式固件代码生成工具。通过 YAML 参数配置，自动生成电流采样、PWM、FOC 控制环等 C 代码骨架。

## 功能

- **参数化配置**：电机额定值、采样电阻、ADC 分辨率、PWM 频率等
- **代码生成**：基于 Jinja2 模板输出 `.c` / `.h` 源文件
- **采样电路辅助**：根据最大电流与目标采样电压自动计算 shunt 阻值与功耗
- **可扩展模板**：支持 STM32 HAL、裸机等风格（按需添加）

## 快速开始

```bash
# 安装依赖
pip install -e .

# 查看示例配置
cat configs/example_drive.yaml

# 生成代码到 output/
drive-codegen generate -c configs/example_drive.yaml -o output/
```

## 项目结构

```
drive-embedded-auto-programming/
├── configs/              # 驱动器参数 YAML
├── src/drive_codegen/    # 生成器核心
├── templates/            # Jinja2 C 代码模板
└── output/               # 生成结果（git 忽略）
```

## 配置示例

见 `configs/example_drive.yaml`：定义 MCU、电流环、采样电阻、PWM 等参数。

## 许可证

MIT
