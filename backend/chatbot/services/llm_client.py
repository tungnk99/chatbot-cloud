"""
Client LLM (OpenAI) với tool calling: quyết định gọi tool interest hoặc savings-rate.
"""

import json
import logging
from typing import TYPE_CHECKING, Any

from openai import AsyncOpenAI

if TYPE_CHECKING:
    from .tools_client import ToolsClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Bạn là trợ lý tư vấn tài chính cá nhân. Trả lời bằng tiếng Việt.
Chủ đề: tiết kiệm, lãi suất, ngân sách cá nhân, nợ, quỹ dự phòng.
Khi cần tính lãi (gốc, lãi suất %, kỳ hạn tháng) hãy dùng tool interest_calculator.
Khi cần tính tỷ lệ tiết kiệm so với thu nhập hãy dùng tool savings_rate.
Trả lời ngắn gọn, rõ ràng; sau khi gọi tool hãy tóm tắt kết quả cho người dùng."""

TOOLS_OPENAI = [
    {
        "type": "function",
        "function": {
            "name": "interest_calculator",
            "description": "Tính lãi đơn hoặc lãi kép. Input: principal (số tiền gốc), rate_percent (lãi suất %/năm), months (kỳ hạn tháng), compound (true=lãi kép, false=lãi đơn).",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Số tiền gốc"},
                    "rate_percent": {"type": "number", "description": "Lãi suất %/năm"},
                    "months": {"type": "number", "description": "Kỳ hạn (tháng)"},
                    "compound": {"type": "boolean", "description": "True = lãi kép", "default": False},
                },
                "required": ["principal", "rate_percent", "months"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "savings_rate",
            "description": "Tính tỷ lệ tiết kiệm so với thu nhập. Input: income (thu nhập), savings (số tiền tiết kiệm).",
            "parameters": {
                "type": "object",
                "properties": {
                    "income": {"type": "number", "description": "Thu nhập"},
                    "savings": {"type": "number", "description": "Số tiền tiết kiệm"},
                },
                "required": ["income", "savings"],
            },
        },
    },
]


class LLMClient:
    """Gọi OpenAI Chat Completions với tool calling."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.model = model

    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools_client: "ToolsClient",
    ) -> tuple[str, list[dict[str, Any]]]:
        """
        Gửi messages tới LLM; nếu LLM trả về tool_calls thì gọi Tools rồi gửi lại.
        Trả về (content_final, tool_calls_made).
        """
        if not self.client:
            return (
                "Chatbot chưa cấu hình API key. Vui lòng cấu hình OPENAI_API_KEY.",
                [],
            )

        all_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        tool_calls_made: list[dict[str, Any]] = []

        max_rounds = 5
        for _ in range(max_rounds):
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=all_messages,
                tools=TOOLS_OPENAI,
                tool_choice="auto",
            )
            choice = response.choices[0]
            msg = choice.message

            if msg.tool_calls:
                all_messages.append(msg)
                for tc in msg.tool_calls:
                    name = tc.function.name
                    try:
                        args = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        args = {}
                    result = await self._call_tool(tools_client, name, args)
                    tool_calls_made.append(
                        {"tool": name, "input": args, "output": result}
                    )
                    all_messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(result),
                        }
                    )
                continue

            return (msg.content or "", tool_calls_made)

        return ("Đã vượt quá số lần gọi tool.", tool_calls_made)

    async def _call_tool(
        self,
        tools_client: "ToolsClient",
        name: str,
        args: dict[str, Any],
    ) -> dict[str, Any]:
        """Gọi một tool theo tên và args."""
        try:
            if name == "interest_calculator":
                return await tools_client.interest(
                    principal=float(args.get("principal", 0)),
                    rate_percent=float(args.get("rate_percent", 0)),
                    months=float(args.get("months", 0)),
                    compound=bool(args.get("compound", False)),
                )
            if name == "savings_rate":
                return await tools_client.savings_rate(
                    income=float(args.get("income", 0)),
                    savings=float(args.get("savings", 0)),
                )
        except Exception as e:
            logger.exception("Tool call failed: %s", e)
            return {"error": str(e)}
        return {"error": f"Unknown tool: {name}"}
