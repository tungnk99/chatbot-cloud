# PRD – Chatbot Tài Chính (Demo)

## 1. Tổng quan

**Sản phẩm**: Chatbot tư vấn / hỏi đáp tài chính cá nhân đơn giản, chạy trên nền Chatbot Cloud (GCP, serverless).

**Mục đích**: Demo khả năng tích hợp domain tài chính vào hệ thống chatbot có auto-scaling, phục vụ môn Cloud Computing.

**Đối tượng người dùng**: Người dùng cuối (demo), giảng viên / người chấm bài.

---

## 2. Phạm vi (Scope) – Chỉ cho demo

- **Trong phạm vi**: Hỏi đáp bằng ngôn ngữ tự nhiên về các chủ đề tài chính cơ bản; một vài công cụ đơn giản (ví dụ tính lãi, gợi ý tiết kiệm).
- **Ngoài phạm vi**: Không kết nối ngân hàng thật, không tư vấn đầu tư chuyên sâu, không thay thế chuyên gia tài chính.

---

## 3. Tính năng chính

### 3.1 Hỏi đáp tài chính cơ bản

- Trả lời câu hỏi về: tiết kiệm, lãi suất, ngân sách cá nhân, nợ, quỹ dự phòng.
- Ví dụ: “Lãi suất gửi tiết kiệm 1 năm là bao nhiêu?”, “Nên dành bao nhiêu % thu nhập để tiết kiệm?”.
- LLM xử lý ngôn ngữ tự nhiên; có thể dùng prompt/system prompt hướng về domain tài chính.

### 3.2 Công cụ hỗ trợ (Tools) – tùy chọn cho demo

- **Tính lãi đơn/ghép**: Input: số tiền gốc, lãi suất %, kỳ hạn → trả về số tiền lãi / tổng nhận được.
- **Tính % thu nhập tiết kiệm**: Input: thu nhập, số tiền tiết kiệm → trả về tỷ lệ % và gợi ý ngắn (đủ cho demo).

Số lượng tool giữ tối thiểu (1–2) để demo nhanh.

### 3.3 Giao diện và trải nghiệm

- Web chat: gửi tin nhắn, nhận phản hồi từ chatbot.
- Lịch sử hội thoại: lưu theo session (theo kiến trúc hiện tại của Chatbot Cloud, ví dụ GCS).

---

## 4. Yêu cầu phi chức năng (tối thiểu cho demo)

- **Hiệu năng**: Phản hồi trong vài giây cho câu hỏi đơn giản.
- **Sẵn sàng**: Service chạy ổn định trong lúc demo (Cloud Run scale theo tải).
- **Bảo mật**: Không lưu thông tin tài chính nhạy cảm thật; không commit API key/secret.

---

## 5. Tiêu chí hoàn thành / Demo thành công

- [ ] User gửi được câu hỏi tài chính qua web và nhận câu trả lời liên quan.
- [ ] (Tùy chọn) Gọi được ít nhất 1 tool (ví dụ tính lãi) từ chatbot và hiển thị kết quả.
- [ ] Hệ thống chạy trên GCP (Cloud Run), có auto-scaling theo mô tả trong README.
- [ ] Có thể trình bày luồng: User → Web → Chatbot → LLM (+ Tools) → Response.

---

## 6. Ràng buộc và giả định

- Dùng LLM có sẵn (OpenAI / Vertex AI / Gemini) qua API.
- Dữ liệu tài chính trong câu trả lời có thể dựa trên kiến thức LLM hoặc số liệu mẫu cố định (ví dụ lãi suất mẫu) cho demo.
- Không cần đăng nhập/user profile phức tạp cho phiên demo; session đơn giản là đủ.

---

*Tài liệu PRD đơn giản cho mục đích demo – có thể bổ sung chi tiết khi mở rộng.*
