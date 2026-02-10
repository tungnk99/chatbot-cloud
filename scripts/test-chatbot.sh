#!/bin/bash
# Script test chatbot với các câu hỏi mẫu
# Usage: ./test-chatbot.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

API_URL="https://chatbot-api-hbfjjbwmsa-as.a.run.app"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🧪 Testing Chatbot with Tool Calls${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Create a test session
echo -e "${YELLOW}Creating test session...${NC}"
SESSION_RESPONSE=$(curl -s -X POST "$API_URL/api/sessions")
SESSION_ID=$(echo "$SESSION_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['session_id'])" 2>/dev/null)

if [ -z "$SESSION_ID" ]; then
  echo -e "${RED}❌ Failed to create session${NC}"
  exit 1
fi

echo -e "${GREEN}✅ Session created: $SESSION_ID${NC}"
echo ""

# Test 1: Interest Calculator
echo -e "${YELLOW}Test 1: Interest Calculator (Lãi đơn)${NC}"
echo -e "${BLUE}Question: Tôi gửi 10 triệu, lãi suất 6.5%/năm, gửi 12 tháng thì lãi bao nhiêu?${NC}"
echo ""

curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Tôi gửi 10 triệu, lãi suất 6.5%/năm, gửi 12 tháng thì lãi bao nhiêu?\"}" \
  | python3 -m json.tool

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 2: Interest Calculator (Compound)
echo -e "${YELLOW}Test 2: Interest Calculator (Lãi kép)${NC}"
echo -e "${BLUE}Question: Gửi 50 triệu, lãi kép 7%/năm, 24 tháng được bao nhiêu?${NC}"
echo ""

curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Gửi 50 triệu, lãi kép 7%/năm, 24 tháng được bao nhiêu?\"}" \
  | python3 -m json.tool

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 3: Savings Rate
echo -e "${YELLOW}Test 3: Savings Rate${NC}"
echo -e "${BLUE}Question: Thu nhập 20 triệu, tiết kiệm được 5 triệu, tỷ lệ tiết kiệm của tôi là bao nhiêu?${NC}"
echo ""

curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Thu nhập 20 triệu, tiết kiệm được 5 triệu, tỷ lệ tiết kiệm của tôi là bao nhiêu?\"}" \
  | python3 -m json.tool

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test 4: General question (no tool call)
echo -e "${YELLOW}Test 4: General Question (Không gọi tool)${NC}"
echo -e "${BLUE}Question: Làm thế nào để tiết kiệm hiệu quả?${NC}"
echo ""

curl -s -X POST "$API_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Làm thế nào để tiết kiệm hiệu quả?\"}" \
  | python3 -m json.tool

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Xem logs để thấy tool calls chi tiết:${NC}"
echo -e "${BLUE}./view-logs.sh chatbot${NC}"
echo ""
