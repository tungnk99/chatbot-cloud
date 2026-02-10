#!/bin/bash
# Script chạy Locust với Web UI để monitor real-time
# Sử dụng: ./run-locust-interactive.sh

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

CHATBOT_URL="${CHATBOT_URL:-https://chatbot-api-hbfjjbwmsa-as.a.run.app}"
PORT="${LOCUST_PORT:-8089}"

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🦗 Locust Interactive Load Testing${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📋 Configuration:${NC}"
echo -e "   Target URL:  ${GREEN}$CHATBOT_URL${NC}"
echo -e "   Web UI Port: ${GREEN}$PORT${NC}"
echo -e "   Web UI URL:  ${GREEN}http://localhost:$PORT${NC}"
echo ""

# Check if locust is installed
if ! command -v locust &> /dev/null; then
    echo -e "${YELLOW}⚠️  Locust not found. Installing...${NC}"
    pip install -r tests/load/requirements.txt
fi

echo -e "${CYAN}🚀 Starting Locust Web UI...${NC}"
echo ""
echo -e "${YELLOW}📊 Recommended Test Profiles:${NC}"
echo ""
echo -e "${BLUE}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│${NC} ${CYAN}Test Profile${NC}  │ ${CYAN}Users${NC} │ ${CYAN}Spawn Rate${NC} │ ${CYAN}Duration${NC}  │"
echo -e "${BLUE}├─────────────────────────────────────────────────┤${NC}"
echo -e "${BLUE}│${NC} Light Load    │  10   │    2/s     │   2-3m   │"
echo -e "${BLUE}│${NC} Medium Load   │  50   │    5/s     │   3-5m   │"
echo -e "${BLUE}│${NC} Heavy Load    │ 100   │   10/s     │   3-5m   │"
echo -e "${BLUE}│${NC} Spike Test    │ 200   │   50/s     │   2-3m   │"
echo -e "${BLUE}└─────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${YELLOW}📝 Instructions:${NC}"
echo -e "   1. Web UI will open at: ${GREEN}http://localhost:$PORT${NC}"
echo -e "   2. Enter number of users and spawn rate"
echo -e "   3. Click ${GREEN}'Start swarming'${NC} to begin test"
echo -e "   4. Monitor real-time charts and statistics"
echo -e "   5. Download reports before stopping"
echo -e "   6. Press ${YELLOW}Ctrl+C${NC} in terminal to stop Locust"
echo ""
echo -e "${CYAN}💡 Tips:${NC}"
echo -e "   • Open GCP Console in another tab to watch scaling live"
echo -e "   • Start with Light Load to see baseline"
echo -e "   • Wait 2-3 minutes between tests for scale-down"
echo -e "   • Take screenshots of both Locust UI and GCP metrics"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Start Locust with web UI
CHATBOT_URL="$CHATBOT_URL" locust \
    -f tests/load/locustfile.py \
    --host="$CHATBOT_URL" \
    --web-port=$PORT \
    --web-host=0.0.0.0
