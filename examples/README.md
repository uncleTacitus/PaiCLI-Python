# PaiCLI-Python Examples

## LangGraph ReAct Demo

`langgraph_react_demo.py` 展示了如何用 LangGraph 实现一个最简洁的 ReAct Agent，
并与 PaiCLI-Python 自带的 ReAct 实现形成对比。

### 安装运行

```bash
export DEEPSEEK_API_KEY=your_key
uv pip install -e ".[langgraph]"
uv run examples/langgraph_react_demo.py
```

### 与 PaiCLI 自带 ReAct 的对比

| 特征 | PaiCLI 自带 ReAct | LangGraph ReAct |
|------|-------------------|-----------------|
| 状态管理 | 自己维护 message 列表 | `MessagesState` + Reducer |
| 路由 | 代码级 for 循环 + 解析 JSON | `StateGraph` + `conditional_edges` |
| 工具执行 | 手写 `ToolRegistry` | `ToolNode` |
| 适用场景 | 嵌入终端 CLI，需要完全控制 trace | 快速搭建原型、利用生态工具 |

### 本例子要点

1. `StateGraph(MessagesState)` 定义完整状态机
2. `agent_node` 调用绑定了 `save_memory` 工具的 LLM
3. `ToolNode([save_memory])` 执行工具
4. `should_continue` 条件边决定是继续还是结束
5. 最后用类似 PaiAgent 里的那个测试用例："记住我叫张三，然后问我今天星期几"
