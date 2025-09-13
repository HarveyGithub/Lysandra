# Lysandra

## 项目简介

Lysandra 是一个基于 **Python** 的 AI 助手框架，旨在通过统一的工具调用接口，实现任务分析、计划、执行以及结果交付的完整闭环。框架内置了多语言支持、任务循环（Task Loop）以及丰富的系统工具（文件操作、Shell、终端交互、用户通知等），可用于自动化日常工作、信息检索、内容生成和代码执行等场景。

> **核心特性**
>
> - **统一工具调用**：所有系统交互（读写文件、执行命令、终端管理、用户交互等）均通过统一的函数调用接口实现，便于 LLM 调度。
> - **任务循环**：基于 LLM 的思考-工具调用-观察-迭代的循环，自动完成复杂任务。
> - **多语言/多模态**：默认中文交互，支持在请求中指定其他语言或模型。
> - **安全约束**：内置伦理与安全检查，防止执行有害指令。
> - **可扩展**：只需在 `Tools/` 目录实现新工具并在 `Tools_Mapping` 中注册，即可扩展功能。

## 项目结构

```
Lysandra/
├── Agent/                 # 核心 Agent 实现
│   ├── Agent.py           # 主循环逻辑
│   └── Terminal.py       # 终端管理器（多终端复用）
├── Config/                # 配置文件
│   ├── model_config.json
│   ├── model_config.json.example
│   └── Tools_Config.json
├── Prompts/               # 预设 Prompt 文本
│   ├── assistant_prompts.md
│   ├── system_prompts.md
│   └── ...
├── Tools/                 # 系统工具实现
│   ├── File_Operation.py  # 文件读写
│   ├── Message_User.py    # 用户交互（Notify/Ask）
│   └── Terminal.py        # Shell/终端相关工具
├── Load_Config.py         # 加载模型与工具配置
├── Load_Prompts.py        # 加载 Prompt 文本
├── Main.py                # 入口脚本
├── requirements.txt       # Python 依赖
├── test.py                # 简单示例测试脚本
└── README.md              # 本说明文档
```

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库（示例）
git clone https://github.com/your-org/Lysandra.git
cd Lysandra

# 建议使用 virtualenv/conda 创建独立环境
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

> **注意**：项目依赖 `openai`（或兼容的 LLM 客户端）、`pyyaml`、`requests` 等，请确保网络能够访问对应的 PyPI 源。

### 2. 配置模型

在 `Config/model_config.json` 中填写你的 LLM 接口信息，例如 OpenAI 的 API Key 与模型名称：

```json
{
  "api_key": "sk-...",
  "base_url": "https://api.openai.com/v1",
  "model": "gpt-4o-mini"
}
```

如果使用本地模型或其他云服务，只需修改对应字段即可。

### 3. 运行示例

```bash
python Main.py
```

程序会提示输入任务，例如：

```
请输入任务: 帮我在当前目录下创建一个 README 并写入项目简介。
```

Lysandra 将自动调用 `File_Operation`、`Notify_User` 等工具完成任务，并在完成后输出结果。

## 核心模块说明

### `Agent/Agent.py`
- **Agent** 类负责维护对话历史 (`self.Messages`)、管理终端 (`self.Terminals`) 并调度工具调用。
- `create_response`：调用 LLM 的 chat/completions 接口，支持流式返回并收集工具调用信息。
- `tackle_tool_calls`：解析 LLM 返回的 tool calls，映射到实际 Python 函数并执行，随后把工具输出写回对话历史。
- `run`：交互式主循环，持续与 LLM 对话直至收到 `idle` 工具指令结束。

### `Tools/`
| 文件 | 功能 | 关键函数 |
|------|------|----------|
| `File_Operation.py` | 读取、写入、追加文件 | `Read_File`, `Write_File` |
| `Message_User.py`   | 与用户交互（通知/提问） | `Notify_User`, `Ask_User` |
| `Terminal.py`       | Shell 命令、终端管理 | `Send_Command`, `Send_Keys`, `View_Terminal`, `Kill_Terminal` |

所有工具均在 `Tools_Mapping`（`Tools/__init__.py`）中注册，`Tools_List` 为 OpenAI 所需的工具描述列表。

### `Config/`
- `model_config.json`：模型连接信息。
- `Tools_Config.json`：可在此配置工具的默认参数或禁用列表。

### `Prompts/`
存放系统 Prompt、assistant Prompt 等文本，`Load_Prompts.py` 会在 Agent 初始化时读取并注入到对话历史中。

## 开发指南

1. **代码规范**：遵循 PEP8，所有函数必须提供类型注解与 docstring。
2. **新增工具**：在 `Tools/` 新建 `.py` 文件，实现对应函数并在 `Tools_Mapping` 中加入映射；同时在 `Load_Config.py` 中更新 `Tools_List`（OpenAI 需要的 JSON schema）。
3. **单元测试**：使用 `pytest` 编写测试，确保新工具的返回格式符合 LLM 期望。
4. **CI**：推荐使用 GitHub Actions 自动运行 `pytest` 并检查代码格式（`flake8`、`black`）。

## 贡献指南

- Fork 本仓库并创建功能分支。
- 编写代码并通过本地测试。
- 提交清晰的 Commit 信息，打开 Pull Request 并在描述中说明变更点。
- CI 检查通过后，维护者将合并 PR。

## 许可证

本项目采用 **MIT License**，详见 `LICENSE` 文件。

---

*本 README 由 Lysandra 自动生成，旨在提供项目概览与使用指引。如有疑问或建议，请提交 Issue 或联系项目维护者。*
