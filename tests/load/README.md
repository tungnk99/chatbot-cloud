# Load Testing với Locust

Load testing cho **Chatbot Cloud System** sử dụng Locust để:
- ✅ Test performance và scalability
- ✅ Chứng minh khả năng auto-scaling
- ✅ Thu thập metrics và evidence

## 📖 Documentation

**→ Đọc Guide Chính: [`../../LOAD_TESTING_GUIDE.md`](../../LOAD_TESTING_GUIDE.md)**

Guide đầy đủ bao gồm:
- Quick start
- Interactive & Automated modes
- Evidence collection
- Demo script cho presentation
- Troubleshooting

## 🚀 Quick Start

### Cài đặt
```bash
pip install -r tests/load/requirements.txt
```

### Chạy Interactive Mode (Recommended)
```bash
# Từ root project
./run-locust-interactive.sh
```
→ Mở browser: http://localhost:8089

### Chạy Automated Mode
```bash
# Từ root project
./run-locust-tests.sh
```

## 📁 Files

- **`locustfile.py`** - Test scenarios cho Locust
- **`requirements.txt`** - Dependencies
- **`test_load_*.py`** - Pytest load tests (optional)

## 🎯 Test Scenarios

### ChatbotUser
Simulate user tương tác với Chatbot:
- Health check
- Create session
- Get messages
- Send chat messages

### ToolsUser  
Test Tools API endpoints:
- Health check
- Interest calculator
- Savings rate calculator

## 🔧 Configuration

Environment variables:
```bash
CHATBOT_URL=https://chatbot-api-xxx.run.app
TOOLS_URL=https://chatbot-tools-xxx.run.app
```

## 📊 Test Profiles

| Profile | Users | Expected Instances |
|---------|-------|-------------------|
| Light   | 10    | 1-2               |
| Medium  | 50    | 3-5               |
| Heavy   | 100   | 7-10              |
| Spike   | 200   | 8-10 (max)        |

## 📚 More Info

**→ Chi tiết: [`LOAD_TESTING_GUIDE.md`](../../LOAD_TESTING_GUIDE.md)**
