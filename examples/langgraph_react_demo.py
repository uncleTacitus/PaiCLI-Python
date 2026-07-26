"""
LangGraph ReAct Demo for PaiCLI-Python

目的：用最小的代码展示 LangGraph 官方 ReAct 循环，
并与 PaiCLI-Python 自带的 ReAct 实现形成对照。

运行前请设置环境变量：
    export DEEPSEEK_API_KEY=your_key

安装依赖：
    uv pip install -e ".[langgraph]"

运行：
    uv run examples/langgraph_react_demo.py

关键节点：
1. StateGraph + MessagesState 定义状态机
2. agent_node 调用 LLM 并绑定工具
3. ToolNode 执行具体工具
4. should_continue 条件边决定是继续还是结束
"""

from __future__ import annotations

import os
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode


# ---------------------------------------------------------------------------
# 1. 工具：记忆存储
# ---------------------------------------------------------------------------
@tool
def save_memory(content: str) -> str:
    """
    Save a user-provided fact into memory.

    Args:
        content: The fact to remember, e.g. "用户名叫张三".
    """
    return f"OK, remembered: {content}"


# ---------------------------------------------------------------------------
# 2. LLM 客户端（使用 DeepSeek 的 OpenAI-compatible 接口）
# ---------------------------------------------------------------------------
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
).bind_tools([save_memory])


# ---------------------------------------------------------------------------
# 3. Graph 节点
# ---------------------------------------------------------------------------
def agent_node(state: MessagesState) -> dict:
    """Agent 节点：调用 LLM，返回消息。"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def should_continue(state: MessagesState) -> Literal["tools", END]:
    """
    条件边：
    - 如果 LLM 返回了 tool_calls，走 tools 边
    - 否则结束循环
    """
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


# ---------------------------------------------------------------------------
# 4. 构建图
# ---------------------------------------------------------------------------
builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode([save_memory]))

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

react_graph = builder.compile()


# ---------------------------------------------------------------------------
# 5. 运行
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        msg = (
            "DEEPSEEK_API_KEY is not set.\n"
            "Please set it before running this demo:\n"
            "    export DEEPSEEK_API_KEY=your_key"
        )
        raise SystemExit(msg)

    messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. "
                "Use the save_memory tool when the user asks you to remember something."
            )
        ),
        HumanMessage(content="记住我叫张三，然后问我今天星期几"),
    ]

    result = react_graph.invoke({"messages": messages})

    print("\n--- LangGraph ReAct Trace ---\n")
    for msg in result["messages"]:
        print(f"[{msg.type}] {msg.content or '(empty)'}")
    print("\n--- Final Answer ---\n")
    print(result["messages"][-1].content)
