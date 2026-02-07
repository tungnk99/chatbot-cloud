# Hướng Dẫn Phát Triển Cho Agent - Dự Án Chatbot Cloud

## 📋 Mục Đích Tài Liệu

Tài liệu này cung cấp các quy định và hướng dẫn cho AI agent khi làm việc với dự án **Chatbot Cloud**. Tuân thủ các quy định này để đảm bảo chất lượng code, tính nhất quán và phù hợp với kiến trúc serverless trên Google Cloud Platform.

**Ngôn ngữ lập trình**: Python (backend và dịch vụ).

---

## 🎯 Bối Cảnh Dự Án

### Loại Dự Án
- Hệ thống chatbot cloud-native có khả năng tự động dãn nở
- Kiến trúc serverless trên Google Cloud Platform (GCP)
- Ứng dụng mức production cho mục đích học tập (môn Cloud Computing)

### Công Nghệ Chính
- **Cloud**: Google Cloud Platform (GCP)
- **Compute**: Google Cloud Run (container serverless)
- **Storage**: Google Cloud Storage (GCS)
- **AI/ML**: Large Language Models (OpenAI / Vertex AI / Gemini)
- **Backend**: Python 3.8 trở lên
- **Infrastructure**: Docker, Terraform (tùy chọn)
- **CI/CD**: GitHub Actions hoặc Cloud Build

### Nguyên Tắc Kiến Trúc
1. **Serverless-first**: Ưu tiên Cloud Run để auto-scaling
2. **Microservices**: Các thành phần ghép nối lỏng (Chatbot, Tools, Storage)
3. **Tối ưu chi phí**: Trả theo sử dụng, scale về 0
4. **Cloud-native**: Dùng các dịch vụ managed của GCP

---

## 📁 Cấu Trúc Dự Án

### Cấu Trúc Thư Mục Chuẩn

- **Backend/**: Toàn bộ mã nguồn backend
  - **chatbot/**: Dịch vụ chatbot chính (Python)
    - **src/**: Mã nguồn (main.py, handlers/, services/, models/, utils/, config.py)
    - **tests/**: Unit test
    - Dockerfile, requirements.txt, README.md
  - **tools/**: Các dịch vụ công cụ mở rộng (mỗi tool là một service Python)
    - Mỗi tool có thư mục riêng: src/, Dockerfile, requirements.txt

- **Frontend/**: Ứng dụng web (giao diện người dùng)
  - Mã nguồn frontend (React/Vue/Angular hoặc framework khác)
  - Dockerfile, package.json (hoặc tương đương)

- **infrastructure/**: IaC (terraform/, scripts/) nếu có

- **.github/workflows/**: Pipeline CI/CD

- **docs/**: Tài liệu (architecture.md, api.md, database.md, prd.md)

- **AGENT.md**, **CONTRIBUTING.md**, **README.md**, **.gitignore**, **cloudbuild.yaml** ở root

---

## 💻 Chuẩn Viết Code

### Nguyên Tắc Chung

1. **Code rõ ràng, dễ đọc**
   - Đặt tên biến, hàm có ý nghĩa; chỉ thêm comment cho logic phức tạp
   - Tuân thủ SOLID

2. **Hàm ngắn gọn**
   - Một trách nhiệm cho mỗi hàm
   - Khuyến nghị tối đa khoảng 50 dòng mỗi hàm; tách logic phức tạp ra hàm riêng

3. **Xử lý lỗi**
   - Luôn bắt và xử lý exception; log kèm ngữ cảnh (request_id, user_id, …)
   - Trả về thông báo lỗi rõ ràng cho người dùng

4. **Bảo mật trước**
   - Không commit secret, API key, credential
   - Dùng biến môi trường hoặc GCP Secret Manager
   - Validate và sanitize mọi input từ người dùng
   - Có rate limiting

### Chuẩn Python

- **Style**: Tuân thủ PEP 8
- **Format**: Dùng Black (độ dài dòng 88), isort cho import
- **Lint**: pylint hoặc flake8
- **Type hints**: Dùng cho signature hàm (Python 3.8+)
- **Docstring**: Dùng chuẩn Google hoặc reStructuredText cho module, class, hàm public

### Phụ Thuộc Python

- Ghi rõ phiên bản trong requirements.txt (ví dụ: fastapi==x.y.z), tránh dùng >= không cần thiết
- Nhóm theo: core (FastAPI, uvicorn, pydantic), GCP (google-cloud-*), LLM (openai / google-cloud-aiplatform), utils (python-dotenv, httpx)

---

## 🐳 Docker

- Base image: python:3.11-slim (hoặc phiên bản đã thống nhất trong dự án)
- Copy requirements.txt trước, cài dependency rồi mới copy source để tận dụng cache
- Chạy bằng user không phải root
- Có HEALTHCHECK trỏ tới endpoint health
- Expose port 8080 cho Cloud Run (hoặc port đã cấu hình)

---

## ☁️ Triển Khai Cloud Run

- **Min instances**: 0 (scale to zero)
- **Max instances**: Theo nhu cầu (ví dụ 10)
- **Memory/CPU**: Phù hợp workload (ví dụ 512Mi, 1 vCPU)
- **Timeout**: Đặt timeout request (ví dụ 60s)
- **Concurrency**: Số request đồng thời trên một instance (ví dụ 80)
- **Secrets**: Dùng GCP Secret Manager, không đưa secret vào env dạng plain text trong config
- **Region**: Ưu tiên asia-southeast1 hoặc theo yêu cầu

---

## 🔧 Thiết Kế API

### RESTful

- Resource dùng danh từ, số nhiều: /conversations, /messages
- URL dùng kebab-case: /user-sessions
- Có version API: /v1/chat, /v2/chat

### HTTP Method

- GET: Lấy dữ liệu
- POST: Tạo mới
- PUT: Cập nhật toàn bộ
- PATCH: Cập nhật một phần
- DELETE: Xóa

### Mã Trạng Thái

- 200: Thành công (GET, PUT, PATCH)
- 201: Tạo mới thành công (POST)
- 204: Xóa thành công (DELETE)
- 400: Dữ liệu đầu vào không hợp lệ
- 401: Chưa xác thực
- 403: Không đủ quyền
- 404: Không tìm thấy
- 429: Vượt rate limit
- 500: Lỗi server
- 503: Dịch vụ tạm thời không khả dụng

### Định Dạng Response

- Thống nhất: có trường status (success/error), data hoặc error (code, message, details)
- Dùng JSON; timestamp theo ISO 8601

---

## 📊 Logging và Giám Sát

- **Log**: Dạng cấu trúc (structured), dễ parse (JSON); gắn request_id, user_id, latency_ms khi có
- **Không log**: Nội dung tin nhắn người dùng, token, secret
- **Metrics cần theo dõi**: request_count, latency (p50/p95/p99), error_rate, llm_call_count, tokens_used, instance_count, cpu/memory
- Dùng Cloud Logging và tận dụng severity (INFO, WARNING, ERROR)

---

## 🧪 Testing

- **Cấu trúc**: unit/, integration/, e2e/; dùng pytest
- **Coverage**: Tối thiểu 80%; các nhánh quan trọng nên đạt 100%
- **Fixture**: Dùng fixture cho client giả (LLM, Storage); mock/AsyncMock cho gọi ngoài
- **Chạy test**: Trước khi commit; tích hợp vào CI/CD
- **Async**: Dùng pytest-asyncio cho hàm async

---

## 🔒 Bảo Mật

- **Secret**: Không hardcode; dùng os.getenv hoặc Secret Manager
- **Input**: Validate bằng Pydantic; sanitize (strip, giới hạn độ dài, ký tự cho phép)
- **Rate limiting**: Áp dụng cho endpoint public (ví dụ /v1/chat)
- **CORS**: Cấu hình allow_origins cụ thể, không dùng "*" ở production
- **HTTPS**: Mọi kết nối ra ngoài dùng HTTPS

---

## 📝 Tài Liệu Code

- **Docstring**: Mô tả mục đích, Args, Returns, Raises (và Example nếu cần) cho hàm public
- **API**: Dùng OpenAPI/Swagger (FastAPI tự sinh); bổ sung mô tả, example cho request/response
- **README**: Mỗi service (Backend/chatbot, Backend/tools, Frontend) có README ngắn về cách chạy và biến môi trường

---

## 🚀 Hiệu Năng

- **Async**: Dùng async/await cho I/O (HTTP, GCS, LLM); tránh blocking event loop
- **Gọi song song**: Khi gọi nhiều tool hoặc nhiều request độc lập thì dùng asyncio.gather
- **Client**: Dùng một AsyncClient (httpx) dùng chung, có timeout và limits (connection pool)
- **Cache**: Cache prompt/system prompt, hoặc dữ liệu đọc nhiều; lưu ý Cloud Run instance có thể bị tái sử dụng nên không lưu state quan trọng chỉ trong memory
- **State**: Không lưu session/state quan trọng trong memory; dùng Storage hoặc database

---

## ⚠️ Cần Tránh

- **Blocking trong async**: Không gọi requests.get/sync IO trong hàm async; dùng httpx async hoặc chạy blocking trong executor
- **State trong memory**: Không dựa vào biến global hoặc dict trong process để lưu session lâu dài
- **Không timeout**: Mọi gọi API bên ngoài phải có timeout (asyncio.wait_for hoặc tham số timeout của client)
- **Log dữ liệu nhạy cảm**: Không log nội dung message, token, API key
- **Commit secret**: Kiểm tra .gitignore và không đưa file .env có secret lên repo

---

## 🔄 Git

- **Branch**: main (production), develop (staging), feature/xxx, bugfix/xxx, hotfix/xxx
- **Commit**: Theo Conventional Commits — type(scope): mô tả ngắn. Type: feat, fix, docs, style, refactor, test, chore, perf
- **Trước khi commit**: Chạy lint, test; không commit secret; không để print/console.log debug thừa

---

## 📋 Trách Nhiệm Agent

### Khi Tạo File Mới

- Kiểm tra cấu trúc thư mục hiện có: **Backend/** (chatbot, tools), **Frontend/** (web)
- Đặt tên file: snake_case cho Python (Backend); thư mục có thể dùng kebab-case
- Thêm import và dependency đúng chỗ
- Thêm docstring và type hints
- Thêm test cho chức năng mới
- Cập nhật docs nếu cần

### Khi Sửa Code

- Hiểu ngữ cảnh trước khi sửa
- Ưu tiên giữ tương thích ngược
- Cập nhật test liên quan
- Kiểm tra side effect
- Giữ phong cách và pattern đang dùng trong dự án

### Khi Debug

- Ưu tiên xem log (Cloud Logging)
- Reproduce bằng Docker Compose nếu có
- Thêm log debug tạm thời và xóa trước khi commit
- Ghi lại nguyên nhân và cách xử lý (trong commit hoặc docs)

### Khi Thêm Dependency

- Chỉ thêm khi cần thiết
- Ghi version cụ thể trong requirements.txt
- Ghi lý do cần dùng (trong commit hoặc comment)
- Kiểm tra license phù hợp dự án

---

## 🎯 Tóm Tắt Nguyên Tắc

1. **Serverless-first**: Thiết kế cho Cloud Run, auto-scaling
2. **Bảo mật**: Không commit secret, validate input, dùng IAM và Secret Manager
3. **Hiệu năng**: Async, cache, connection pool; không block event loop
4. **Quan sát**: Log có cấu trúc, metrics, cảnh báo
5. **Testing**: Coverage cao, có integration test
6. **Tài liệu**: Docstring rõ, API docs, README
7. **Clean code**: SOLID, DRY, dễ đọc
8. **Cloud-native**: Tận dụng dịch vụ managed của GCP

---

## 📚 Tài Liệu Tham Khảo

- Nội bộ: docs/architecture.md, docs/api.md, docs/database.md, docs/prd.md
- Ngoài: Cloud Run Best Practices (GCP), PEP 8, FastAPI docs, Google Cloud SDK

---

## ✅ Checklist Cho Agent

Trước khi hoàn thành task:

- [ ] Code tuân thủ quy định trong tài liệu này
- [ ] Không hardcode secret/credential
- [ ] Xử lý lỗi và log đầy đủ
- [ ] Có test và test pass
- [ ] Cập nhật tài liệu nếu cần
- [ ] Cấu hình Docker và Cloud Run hợp lý
- [ ] Đã xem xét bảo mật và hiệu năng

---

**Lưu ý**: Đây là dự án học tập mức production. Viết code như sẽ triển khai cho người dùng thật: chất lượng, bảo mật và khả năng mở rộng đều quan trọng.

**Cập nhật lần cuối**: 7 tháng 2, 2026
