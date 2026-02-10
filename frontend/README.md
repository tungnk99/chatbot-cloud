# Frontend (Streamlit)

Giao diện chat với AI chatbot tài chính, hỗ trợ 7 công cụ tính toán:
- 💰 **Interest Calculator** - Tính lãi đơn/lãi kép
- 📊 **Savings Rate** - Tính tỷ lệ tiết kiệm
- 🏦 **Loan Payment** - Tính khoản trả góp hàng tháng
- 📈 **Investment Return** - Tính lợi nhuận đầu tư với đóng góp định kỳ
- 💼 **Budget Breakdown** - Phân tích ngân sách theo quy tắc 50/30/20
- 💱 **Currency Converter** - Chuyển đổi 10 loại tiền tệ
- 🆘 **Emergency Fund** - Tính quỹ dự phòng cần thiết

## Chạy local

1. Chạy **Chatbot** (Backend/chatbot) trước, ví dụ port 8080. Hoặc đặt `MOCK_API=true` để test giao diện không cần backend.
2. Đặt biến môi trường `CHATBOT_API_URL=http://localhost:8080` (hoặc tạo `.env`).
3. Chạy:

```bash
cd Frontend
pip install -r requirements.txt
streamlit run app.py
```

Mở http://localhost:8501 (hoặc port Streamlit báo).

## Biến môi trường

| Biến | Mô tả |
|------|--------|
| `CHATBOT_API_URL` | URL Chatbot API (mặc định http://localhost:8080) |
| `MOCK_API` | `true` hoặc `1`: test giao diện không cần backend (trả về dữ liệu giả) |

## Docker

```bash
docker build -t chatbot-frontend .
docker run -p 8080:8080 -e CHATBOT_API_URL=http://host.docker.internal:8080 chatbot-frontend
```

Truy cập http://localhost:8080.

## Triển khai Cloud Run

Deploy riêng; cấu hình `CHATBOT_API_URL` trỏ tới URL Chatbot service.

## Tính năng UI

### 🎨 Theme & Design
- Dark theme với gradient background
- Chat bubbles với border glow effect
- Sidebar với lịch sử phiên chat
- Responsive layout (desktop & mobile)

### 💡 Smart Suggestions
- 8 gợi ý câu hỏi mẫu bao phủ tất cả 7 tools
- Click để tự động điền câu hỏi
- Layout 2 cột responsive

### 🔧 Tool Visibility
- Expander "Công cụ đã dùng" hiển thị tool calls
- JSON output format đẹp
- Dễ debug và kiểm tra kết quả

### 📱 Session Management
- Tạo phiên mới
- Xem lịch sử phiên (30 phiên gần nhất)
- Switch giữa các phiên
- Hiển thị session_id

### 🧪 Mock Mode
- Test UI không cần backend
- Set `MOCK_API=true` để bật
- Trả về dữ liệu giả để demo

## Ví dụ câu hỏi

```
Tính lãi 100 triệu gửi 12 tháng, lãi suất 6%/năm?
Vay 500 triệu lãi 8%/năm trả góp 10 năm, mỗi tháng trả bao nhiêu?
Thu nhập 20 triệu/tháng nên phân bổ ngân sách thế nào?
1000 USD bằng bao nhiêu tiền Việt?
```
