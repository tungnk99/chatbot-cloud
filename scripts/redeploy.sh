#!/bin/bash
# Script tự động build và deploy lại chatbot-cloud lên GCP Cloud Run
# Usage: ./redeploy.sh [--skip-build] [--auto-approve]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project info
PROJECT_ID="chatbot-cloud-n9"
REGION="asia-southeast1"

# Parse arguments
SKIP_BUILD=false
AUTO_APPROVE=false

for arg in "$@"; do
  case $arg in
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    --auto-approve)
      AUTO_APPROVE=true
      shift
      ;;
    --help|-h)
      echo "Usage: ./redeploy.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --skip-build      Bỏ qua bước build Docker images"
      echo "  --auto-approve    Tự động approve terraform apply (không cần confirm)"
      echo "  --help, -h        Hiển thị help"
      echo ""
      echo "Steps:"
      echo "  1. Build Docker images (tools, chatbot, frontend)"
      echo "  2. Deploy infrastructure với Terraform"
      echo "  3. Force update Cloud Run services với images mới"
      exit 0
      ;;
  esac
done

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}🚀 Chatbot Cloud - Redeploy Script${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "cloudbuild.yaml" ]; then
  echo -e "${RED}❌ Error: cloudbuild.yaml not found!${NC}"
  echo -e "${YELLOW}Please run this script from project root directory${NC}"
  exit 1
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
  echo -e "${RED}❌ Error: gcloud CLI not found!${NC}"
  echo -e "${YELLOW}Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install${NC}"
  exit 1
fi

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
  echo -e "${RED}❌ Error: terraform not found!${NC}"
  echo -e "${YELLOW}Please install Terraform: https://www.terraform.io/downloads${NC}"
  exit 1
fi

# Step 1: Build and push Docker images
if [ "$SKIP_BUILD" = false ]; then
  echo -e "${YELLOW}📦 Step 1/3: Building Docker images...${NC}"
  echo -e "${BLUE}Building: tools, chatbot, frontend${NC}"
  echo ""
  
  gcloud builds submit --config=cloudbuild.yaml .
  
  if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Build successful!${NC}"
  else
    echo ""
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}⏭️  Skipping build step (--skip-build)${NC}"
fi

echo ""
echo -e "${YELLOW}🚀 Step 2/3: Deploying to Cloud Run with Terraform...${NC}"
echo ""

# Navigate to terraform directory
cd infrastructure/terraform

# Step 2: Deploy with Terraform
if [ "$AUTO_APPROVE" = true ]; then
  terraform apply -auto-approve
else
  terraform apply
fi

if [ $? -eq 0 ]; then
  echo ""
  echo -e "${GREEN}✅ Terraform deployment successful!${NC}"
else
  echo ""
  echo -e "${RED}❌ Terraform deployment failed!${NC}"
  exit 1
fi

# Navigate back to root
cd ../..

echo ""
echo -e "${YELLOW}🔄 Step 3/3: Force updating services with new images...${NC}"
echo ""

# Step 3: Force update services to pull new :latest images
ARTIFACT_REPO="asia-southeast1-docker.pkg.dev/$PROJECT_ID/chatbot-cloud"

echo -e "${BLUE}Updating chatbot-tools...${NC}"
gcloud run services update chatbot-tools \
  --region=$REGION \
  --image=$ARTIFACT_REPO/tools:latest \
  --quiet

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ chatbot-tools updated!${NC}"
else
  echo -e "${RED}❌ chatbot-tools update failed!${NC}"
fi

echo ""
echo -e "${BLUE}Updating chatbot-api...${NC}"
gcloud run services update chatbot-api \
  --region=$REGION \
  --image=$ARTIFACT_REPO/chatbot:latest \
  --quiet

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ chatbot-api updated!${NC}"
else
  echo -e "${RED}❌ chatbot-api update failed!${NC}"
fi

echo ""
echo -e "${BLUE}Updating chatbot-frontend...${NC}"
gcloud run services update chatbot-frontend \
  --region=$REGION \
  --image=$ARTIFACT_REPO/frontend:latest \
  --quiet

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ chatbot-frontend updated!${NC}"
else
  echo -e "${RED}❌ chatbot-frontend update failed!${NC}"
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}🎉 Redeploy completed successfully!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Get service URLs
echo -e "${YELLOW}🌐 Service URLs:${NC}"
cd infrastructure/terraform
FRONTEND_URL=$(terraform output -raw cloud_run_frontend_url 2>/dev/null)
CHATBOT_URL=$(terraform output -raw cloud_run_chatbot_url 2>/dev/null)
TOOLS_URL=$(terraform output -raw cloud_run_tools_url 2>/dev/null)
cd ../..

echo ""
echo -e "${GREEN}Frontend:${NC}   $FRONTEND_URL"
echo -e "${GREEN}Chatbot API:${NC} $CHATBOT_URL"
echo -e "${GREEN}Tools API:${NC}   $TOOLS_URL"
echo ""

# Show useful commands
echo -e "${YELLOW}📝 Useful commands:${NC}"
echo ""
echo -e "${BLUE}# View logs (Chatbot API):${NC}"
echo "gcloud run services logs read chatbot-api --region=$REGION --limit=100"
echo ""
echo -e "${BLUE}# View logs real-time:${NC}"
echo "gcloud run services logs tail chatbot-api --region=$REGION"
echo ""
echo -e "${BLUE}# View logs (Tools API):${NC}"
echo "gcloud run services logs read chatbot-tools --region=$REGION --limit=100"
echo ""
echo -e "${BLUE}# Test chatbot:${NC}"
echo "curl -X POST $CHATBOT_URL/chat \\"
echo '  -H "Content-Type: application/json" \\'
echo '  -d '"'"'{"message": "Tôi gửi 10 triệu, lãi suất 6.5%/năm, 12 tháng thì lãi bao nhiêu?"}'"'"
echo ""
echo -e "${BLUE}# View service revisions:${NC}"
echo "gcloud run services describe chatbot-api --region=$REGION --format='value(status.latestReadyRevisionName)'"
echo ""
