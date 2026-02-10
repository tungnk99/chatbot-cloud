#!/bin/bash
# Script xem logs của các services trên Cloud Run
# Usage: ./view-logs.sh [service] [--tail]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

REGION="asia-southeast1"
SERVICE="$1"
MODE="$2"

# Function to show usage
show_usage() {
  echo -e "${BLUE}Usage: ./view-logs.sh [service] [--tail]${NC}"
  echo ""
  echo "Services:"
  echo "  chatbot    - Xem logs của Chatbot API"
  echo "  tools      - Xem logs của Tools API"
  echo "  frontend   - Xem logs của Frontend"
  echo "  all        - Xem logs của tất cả services (không hỗ trợ --tail)"
  echo ""
  echo "Options:"
  echo "  --tail     - Xem logs real-time (live stream)"
  echo "  --help     - Hiển thị help"
  echo ""
  echo "Examples:"
  echo "  ./view-logs.sh chatbot          # Xem 100 logs cuối của chatbot"
  echo "  ./view-logs.sh chatbot --tail   # Xem logs chatbot real-time"
  echo "  ./view-logs.sh all              # Xem logs của tất cả services"
}

# Function to view logs
view_logs() {
  local service_name=$1
  local service_display=$2
  
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}📋 Logs: $service_display${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  if [ "$MODE" = "--tail" ]; then
    echo -e "${YELLOW}🔴 Live streaming logs... (Ctrl+C to stop)${NC}"
    echo ""
    gcloud run services logs tail "$service_name" --region="$REGION"
  else
    gcloud run services logs read "$service_name" --region="$REGION" --limit=100
  fi
}

# Check arguments
if [ -z "$SERVICE" ] || [ "$SERVICE" = "--help" ] || [ "$SERVICE" = "-h" ]; then
  show_usage
  exit 0
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
  echo -e "${RED}❌ Error: gcloud CLI not found!${NC}"
  exit 1
fi

# View logs based on service
case "$SERVICE" in
  chatbot)
    view_logs "chatbot-api" "Chatbot API"
    ;;
  tools)
    view_logs "chatbot-tools" "Tools API"
    ;;
  frontend)
    view_logs "chatbot-frontend" "Frontend"
    ;;
  all)
    if [ "$MODE" = "--tail" ]; then
      echo -e "${RED}❌ Error: --tail mode không hỗ trợ cho 'all'${NC}"
      echo -e "${YELLOW}Vui lòng chỉ định một service cụ thể${NC}"
      exit 1
    fi
    
    view_logs "chatbot-tools" "Tools API"
    echo ""
    view_logs "chatbot-api" "Chatbot API"
    echo ""
    view_logs "chatbot-frontend" "Frontend"
    ;;
  *)
    echo -e "${RED}❌ Unknown service: $SERVICE${NC}"
    echo ""
    show_usage
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
