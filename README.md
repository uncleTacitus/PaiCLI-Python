<div align="center">

# PaiCLI

**终端中的 AI Agent CLI — 面向真实项目开发场景**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)

</div>

> **PaiCLI-Python** 是一个运行在终端里的 AI Agent CLI，面向真实项目开发场景：读写文件、搜索代码、执行命令、联网检索、调用 MCP 工具、保存记忆、生成快照、恢复现场，并通过 Runtime API 对外提供线程、turn、事件和后台任务能力。

---

## 功能特性

### Agent 模式
| 模式 | 说明 |
|------|------|
| **ReAct** | Observe → Think → Act 循环，适合简单线性任务 |
| **Plan-and-Execute** | Planner 生成 DAG，按依赖批次并行执行 |
| **Multi-Agent** | Planner + Worker + Reviewer 三种角色协作 |

### 核心能力
- 交互式终端 Agent（基于 Rich + prompt-toolkit）
- ReAct 工具调用循环，支持 thinking / tool call / tool result / final output / usage 事件
- Plan-and-Execute 模式，Planner 生成 DAG 并按依赖批次并行执行
- Multi-Agent 协作，包含 Planner / Worker / Reviewer，支持 Review 重试
- 内置工具：文件读写、Shell 执行、grep/glob 搜索、网页检索、代码搜索等
- HITL 人工确认 + 命令/路径安全策略 + JSONL 审计日志

### MCP
- MCP Client：支持 stdio 和 Streamable HTTP 两种传输
- 自身可作为 MCP Server 暴露内置工具
- Chrome DevTools MCP 配置助手

### RAG & 记忆
- 代码向量化（Embedding），SQLite 持久化 + 余弦相似度语义检索
- 代码分块（文件/类/方法粒度）与 AST 解析
- 代码关系图谱（extends / implements / imports / calls / contains）
- 短期记忆（对话上下文）、长期记忆（SQLite 跨会话持久化）
- Agent Run 前后自动创建快照，支持恢复现场

### Skill 系统
- 支持内置 / 用户级 / 项目级 Skill，三级渐进式加载
- load_skill 懒加载注入

### Runtime API
- 线程、turn、事件日志、持久化后台任务
- 支持本地/远程图片输入，模型能力自动降级

---

## 快速开始

```bash
# 克隆
git clone https://github.com/uncleTacitus/PaiCLI-Python.git
cd PaiCLI-Python

# 安装依赖
uv sync --extra dev

# 启动交互模式
uv run paicli

# 单次查询
uv run paicli -p "帮我总结这个项目"

# 检查环境
uv run paicli doctor --cwd .
```

## 环境要求

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- 可选：`rg` 用于更快的本地搜索

## 架构

```
User Input → Agent Loop → Tools/MCP → Result
              │
              ├── ReAct Mode: Observe → Think → Act (循环)
              ├── Plan-and-Execute: Planner → Workers → Reviewer
              └── Multi-Agent: Planner + Worker + Reviewer 协同
```

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  LLM Client  │────▶│  Agent Loop  │────▶│  Tool        │
│ (OpenAI/    │     │  (ReAct/PnE/ │     │  Registry    │
│  DeepSeek)  │◀────│   Multi-Agent)│◀────│  + MCP       │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────┴───────┐
                    │  Memory      │
                    │  (SQLite)    │
                    │  + Snapshot  │
                    └──────────────┘
```

---

## 项目结构

```
PaiCLI-Python/
├── src/
│   ├── paicli/           # 主入口
│   │   ├── agent/        # Agent 核心（ReAct/PnE/Multi-Agent）
│   │   ├── tools/        # 内置工具实现
│   │   ├── mcp/          # MCP Client/Server
│   │   ├── memory/       # 记忆系统
│   │   ├── rag/          # RAG 与代码索引
│   │   ├── skill/        # Skill 系统
│   │   └── api/          # Runtime API
│   └── ...
├── tests/                # 测试
├── docs/                 # 文档
└── README.md
```

---

## 技术栈

- **语言**: Python 3.12, asyncio
- **LLM**: OpenAI-compatible API, DeepSeek / OpenAI / GLM / Qwen
- **CLI**: Rich, prompt-toolkit
- **存储**: SQLite, JSONL
- **协议**: MCP SDK (stdio + Streamable HTTP)
- **搜索**: ripgrep, 余弦相似度

---

## 许可证

MIT
