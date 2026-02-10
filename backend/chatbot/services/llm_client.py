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
Chủ đề: tiết kiệm, lãi suất, ngân sách cá nhân, nợ, quỹ dự phòng, đầu tư, vay vốn.

Các công cụ bạn có thể sử dụng:
- interest_calculator: Tính lãi đơn/lãi kép
- savings_rate: Tính tỷ lệ tiết kiệm so với thu nhập
- loan_payment: Tính khoản trả góp hàng tháng cho khoản vay
- investment_return: Tính lợi nhuận đầu tư với đóng góp định kỳ
- budget_breakdown: Phân tích ngân sách theo quy tắc 50/30/20
- currency_convert: Chuyển đổi tiền tệ
- emergency_fund: Tính quỹ dự phòng cần thiết

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
    {
        "type": "function",
        "function": {
            "name": "loan_payment",
            "description": "Tính khoản trả góp hàng tháng cho khoản vay. Input: principal (số tiền vay), annual_rate (lãi suất %/năm), months (số tháng trả góp).",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Số tiền vay"},
                    "annual_rate": {"type": "number", "description": "Lãi suất %/năm"},
                    "months": {"type": "integer", "description": "Số tháng trả góp"},
                },
                "required": ["principal", "annual_rate", "months"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "investment_return",
            "description": "Tính lợi nhuận đầu tư với đóng góp định kỳ. Input: initial_amount (số tiền ban đầu), monthly_contribution (đóng góp hàng tháng), annual_return (lợi nhuận %/năm), years (số năm đầu tư).",
            "parameters": {
                "type": "object",
                "properties": {
                    "initial_amount": {"type": "number", "description": "Số tiền ban đầu"},
                    "monthly_contribution": {"type": "number", "description": "Đóng góp hàng tháng"},
                    "annual_return": {"type": "number", "description": "Lợi nhuận %/năm"},
                    "years": {"type": "number", "description": "Số năm đầu tư"},
                },
                "required": ["initial_amount", "monthly_contribution", "annual_return", "years"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "budget_breakdown",
            "description": "Phân tích ngân sách theo quy tắc 50/30/20. Input: monthly_income (thu nhập hàng tháng). Output: 50% nhu cầu thiết yếu, 30% mong muốn, 20% tiết kiệm.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_income": {"type": "number", "description": "Thu nhập hàng tháng"},
                },
                "required": ["monthly_income"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "currency_convert",
            "description": "Chuyển đổi tiền tệ. Hỗ trợ: USD, VND, EUR, GBP, JPY, CNY, KRW, THB, SGD, AUD. Input: amount (số tiền), from_currency (mã tiền tệ nguồn), to_currency (mã tiền tệ đích).",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Số tiền"},
                    "from_currency": {"type": "string", "description": "Mã tiền tệ nguồn (VND, USD, EUR, ...)"},
                    "to_currency": {"type": "string", "description": "Mã tiền tệ đích (VND, USD, EUR, ...)"},
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "emergency_fund",
            "description": "Tính quỹ dự phòng khẩn cấp cần thiết. Input: monthly_expenses (chi tiêu hàng tháng), months_coverage (số tháng dự phòng, 3-12 tháng, mặc định 6).",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_expenses": {"type": "number", "description": "Chi tiêu hàng tháng"},
                    "months_coverage": {"type": "integer", "description": "Số tháng dự phòng (3-12)", "default": 6},
                },
                "required": ["monthly_expenses"],
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
                logger.info("🔧 LLM đã quyết định gọi %d tool(s)", len(msg.tool_calls))
                all_messages.append(msg)
                for tc in msg.tool_calls:
                    name = tc.function.name
                    try:
                        args = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        logger.warning("⚠️  Parse tool arguments thất bại: %s", tc.function.arguments)
                        args = {}
                    
                    logger.info("📞 Đang gọi tool: %s với params: %s", name, args)
                    result = await self._call_tool(tools_client, name, args)
                    logger.info("✅ Tool %s trả về kết quả: %s", name, result)
                    
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
        logger.debug("🔍 _call_tool: name=%s, args=%s", name, args)
        try:
            if name == "interest_calculator":
                logger.info("💰 Gọi interest_calculator với principal=%s, rate=%s%%, months=%s, compound=%s",
                           args.get("principal"), args.get("rate_percent"), 
                           args.get("months"), args.get("compound"))
                return await tools_client.interest(
                    principal=float(args.get("principal", 0)),
                    rate_percent=float(args.get("rate_percent", 0)),
                    months=float(args.get("months", 0)),
                    compound=bool(args.get("compound", False)),
                )
            if name == "savings_rate":
                logger.info("📊 Gọi savings_rate với income=%s, savings=%s",
                           args.get("income"), args.get("savings"))
                return await tools_client.savings_rate(
                    income=float(args.get("income", 0)),
                    savings=float(args.get("savings", 0)),
                )
            if name == "loan_payment":
                logger.info("🏦 Gọi loan_payment với principal=%s, rate=%s%%, months=%s",
                           args.get("principal"), args.get("annual_rate"), args.get("months"))
                return await tools_client.loan_payment(
                    principal=float(args.get("principal", 0)),
                    annual_rate=float(args.get("annual_rate", 0)),
                    months=int(args.get("months", 0)),
                )
            if name == "investment_return":
                logger.info("📈 Gọi investment_return với initial=%s, monthly=%s, return=%s%%, years=%s",
                           args.get("initial_amount"), args.get("monthly_contribution"),
                           args.get("annual_return"), args.get("years"))
                return await tools_client.investment_return(
                    initial_amount=float(args.get("initial_amount", 0)),
                    monthly_contribution=float(args.get("monthly_contribution", 0)),
                    annual_return=float(args.get("annual_return", 0)),
                    years=float(args.get("years", 0)),
                )
            if name == "budget_breakdown":
                logger.info("💼 Gọi budget_breakdown với monthly_income=%s",
                           args.get("monthly_income"))
                return await tools_client.budget_breakdown(
                    monthly_income=float(args.get("monthly_income", 0)),
                )
            if name == "currency_convert":
                logger.info("💱 Gọi currency_convert với amount=%s %s -> %s",
                           args.get("amount"), args.get("from_currency"), args.get("to_currency"))
                return await tools_client.currency_convert(
                    amount=float(args.get("amount", 0)),
                    from_currency=str(args.get("from_currency", "")),
                    to_currency=str(args.get("to_currency", "")),
                )
            if name == "emergency_fund":
                logger.info("🆘 Gọi emergency_fund với monthly_expenses=%s, months=%s",
                           args.get("monthly_expenses"), args.get("months_coverage", 6))
                return await tools_client.emergency_fund(
                    monthly_expenses=float(args.get("monthly_expenses", 0)),
                    months_coverage=int(args.get("months_coverage", 6)),
                )
        except Exception as e:
            logger.exception("❌ Tool call thất bại: %s", e)
            return {"error": str(e)}
        
        logger.error("❌ Tool không tồn tại: %s", name)
        return {"error": f"Unknown tool: {name}"}
