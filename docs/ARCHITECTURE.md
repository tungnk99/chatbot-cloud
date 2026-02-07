# Kiến Trúc Hệ Thống Chatbot Trên Cloud

## Tổng Quan

Tài liệu này mô tả kiến trúc của hệ thống chatbot dựa trên nền tảng Google Cloud Platform (GCP). Hệ thống tận dụng công nghệ serverless computing, mô hình ngôn ngữ lớn (LLM), và cloud storage để cung cấp giao diện hội thoại thông minh.

## Sơ Đồ Kiến Trúc Hệ Thống

![Cloud Architecture](./sources/Cloud%20Architecture.drawio.png)

## Các Thành Phần

### 1. User (Người Dùng)
**Mô tả**: Điểm đầu vào để người dùng cuối tương tác với hệ thống chatbot.

**Trách nhiệm**:
- Gửi câu hỏi/yêu cầu đến hệ thống
- Nhận và xem phản hồi từ chatbot
- Quản lý phiên làm việc của người dùng

**Công nghệ**: Giao diện web có thể truy cập qua trình duyệt

---

### 2. Web Application (Ứng Dụng Web)
**Mô tả**: Lớp ứng dụng frontend xử lý tương tác người dùng và giao tiếp với các dịch vụ backend.

**Trách nhiệm**:
- Xử lý tin nhắn từ người dùng
- Chuyển tiếp yêu cầu đến dịch vụ Chatbot
- Nhận và hiển thị phản hồi cho người dùng
- Quản lý trạng thái ứng dụng và logic giao diện

**Giao tiếp**:
- **Đầu vào**: Tin nhắn từ người dùng
- **Đầu ra**: Phản hồi từ chatbot

**Triển khai**: Ứng dụng được đóng gói trong container

---

### 3. Chatbot (Google Cloud Run)
**Mô tả**: Dịch vụ chatbot cốt lõi được triển khai dưới dạng serverless container trên Google Cloud Run. Đây là lớp điều phối chính giữa LLM, Tools, và Storage.

**Trách nhiệm**:
- Nhận tin nhắn từ Web Application
- Thực hiện prompting và reasoning
- Gọi các công cụ (tools) khi cần thiết
- Lưu trữ và truy xuất dữ liệu từ Storage
- Giao tiếp với LLM để hiểu và tạo ngôn ngữ tự nhiên
- Trả về phản hồi đã được định dạng

**Đặc điểm chính**:
- **Serverless**: Tự động scale theo nhu cầu
- **Container-based**: Chạy dưới dạng ứng dụng được đóng gói
- **Điều phối**: Quản lý luồng dữ liệu giữa LLM, Tools và Storage

**Tương tác**:
- **Web Application** → Message → **Chatbot** → Response → **Web Application**
- **Chatbot** ↔ **LLM**: Gửi yêu cầu prompting/reasoning và nhận phản hồi
- **Chatbot** → **Tools**: Gọi các công cụ khi cần chức năng cụ thể
- **Chatbot** ↔ **Storage**: Lưu trữ và truy xuất dữ liệu

**Nền tảng**: Google Cloud Run

---

### 4. LLM (Large Language Model - Mô Hình Ngôn Ngữ Lớn)
**Mô tả**: Thành phần trí tuệ nhân tạo cung cấp khả năng hiểu và tạo ngôn ngữ tự nhiên.

**Trách nhiệm**:
- Xử lý các truy vấn bằng ngôn ngữ tự nhiên
- Tạo phản hồi giống con người
- Thực hiện suy luận và ra quyết định
- Cung cấp câu trả lời có ngữ cảnh

**Mô hình tương tác**:
- Nhận yêu cầu prompting/reasoning từ Chatbot
- Trả về phản hồi và khuyến nghị đã được tạo

**Công nghệ**: Dịch vụ LLM trên cloud (ví dụ: Vertex AI, OpenAI API, hoặc các nhà cung cấp LLM khác)

---

### 5. Tools (Công Cụ - Google Cloud Run)
**Mô tả**: Tập hợp các chức năng và dịch vụ chuyên biệt được triển khai trên Cloud Run để mở rộng khả năng của chatbot.

**Trách nhiệm**:
- Cung cấp chức năng cụ thể ngoài khả năng hội thoại cơ bản
- Thực thi các tác vụ chuyên biệt (ví dụ: tính toán, xử lý dữ liệu, tích hợp API)
- Trả về phản hồi có cấu trúc cho Chatbot

**Mô hình tương tác**:
- **Chatbot** → Tool Call → **Tools**
- **Tools** → Response → **Chatbot**

**Ví dụ về Tools**:
- Chức năng truy xuất dữ liệu
- Dịch vụ tính toán
- Tích hợp API bên ngoài
- Tiện ích xử lý tài liệu

**Nền tảng**: Google Cloud Run (serverless functions/microservices)

---

### 6. Storage (Lưu Trữ - Cloud Storage)
**Mô tả**: Dịch vụ Google Cloud Storage để lưu trữ dữ liệu, lịch sử hội thoại và các tài nguyên khác.

**Trách nhiệm**:
- Lưu trữ lịch sử hội thoại và ngữ cảnh
- Lưu giữ dữ liệu và tùy chọn của người dùng
- Lưu trữ tài liệu, file và media
- Cung cấp khả năng truy xuất dữ liệu

**Mô hình tương tác**:
- **Chatbot** → Store → **Storage**: Lưu dữ liệu
- **Chatbot** → Retrieve → **Storage**: Lấy dữ liệu

**Các loại dữ liệu**:
- Nhật ký hội thoại
- Hồ sơ và tùy chọn người dùng
- Tài liệu và file được tải lên
- Dữ liệu cấu hình
- Phân tích và số liệu thống kê

**Nền tảng**: Google Cloud Storage

---

### 7. Pub/Sub (Hàng đợi – Google Cloud Pub/Sub)
**Mô tả**: Hàng đợi tin nhắn để xử lý chat **bất đồng bộ**. Khi chatbot cần gọi LLM nặng (mất nhiều thời gian), tin nhắn được đẩy vào topic thay vì xử lý đồng bộ, tránh treo kết nối người dùng.

**Trách nhiệm**:
- Nhận tin nhắn từ Chatbot (publish)
- Push message tới endpoint Chatbot (`/api/pubsub/chat-handler`) để gọi LLM và lưu kết quả
- Cho phép client poll GET messages để lấy phản hồi sau khi xử lý xong

**Luồng bất đồng bộ**:
1. **User** gửi tin nhắn; **Frontend** gọi POST `/api/chat?async=1`
2. **Chatbot** lưu tin nhắn user, publish payload (session_id, message) lên **Pub/Sub** topic `chat-requests`, trả về `status: "pending"`
3. **Pub/Sub** push message tới **Chatbot** endpoint `/api/pubsub/chat-handler`
4. **Chatbot** gọi LLM, lưu assistant message vào **Storage**, trả về 200 (ack)
5. **Frontend** poll GET `/api/sessions/{id}/messages` cho tới khi có assistant reply

**Nền tảng**: Google Cloud Pub/Sub (topic + push subscription)

---

## Luồng Dữ Liệu

### 1. Luồng Truy Vấn Của Người Dùng
1. **Người dùng** gửi tin nhắn qua **Web Application**
2. **Web Application** chuyển tiếp tin nhắn đến dịch vụ **Chatbot**
3. **Chatbot** xử lý yêu cầu và gửi prompting/reasoning request đến **LLM**
4. **LLM** phân tích truy vấn và trả về phản hồi kèm theo khuyến nghị về công cụ cần dùng
5. Nếu cần thiết, **Chatbot** gọi các tool calls đến dịch vụ **Tools**
6. **Tools** thực thi chức năng được yêu cầu và trả về phản hồi
7. **Chatbot** có thể lưu dữ liệu liên quan vào **Storage**
8. **Chatbot** gửi phản hồi cuối cùng về **Web Application**
9. **Web Application** hiển thị phản hồi cho **Người dùng**

### 2. Luồng Truy Xuất Dữ Liệu
1. **Chatbot** nhận yêu cầu cần dữ liệu lịch sử
2. **Chatbot** gửi yêu cầu retrieve đến **Storage**
3. **Storage** trả về dữ liệu được yêu cầu
4. **Chatbot** sử dụng dữ liệu này để cung cấp ngữ cảnh cho **LLM**
5. Phản hồi được tạo và gửi lại cho người dùng

---

## Cấu Trúc Mã Nguồn

Dự án tổ chức mã nguồn theo hai nhánh chính:

- **Backend/**: Toàn bộ dịch vụ phía server
  - **chatbot/**: Dịch vụ chatbot cốt lõi (Python), triển khai trên Cloud Run
  - **tools/**: Các microservice công cụ mở rộng (Python), mỗi tool có thể deploy riêng trên Cloud Run
- **Frontend/**: Ứng dụng web (giao diện người dùng), đóng gói container và triển khai trên Cloud Run

Luồng triển khai: User tương tác với **Frontend** → Frontend gọi API **Backend (Chatbot)** → Chatbot gọi **LLM** và **Backend (Tools)** khi cần, đồng thời đọc/ghi **Storage**.

---

## Công Nghệ Sử Dụng

### Nền Tảng Cloud
- **Google Cloud Platform (GCP)**: Nhà cung cấp cloud chính
- **Google Cloud Run**: Nền tảng serverless container cho Chatbot và Tools
- **Google Cloud Storage**: Object storage để lưu trữ dữ liệu
- **Google Cloud Pub/Sub**: Hàng đợi tin nhắn cho xử lý chat bất đồng bộ (tránh treo khi LLM nặng)

### Công Nghệ Chính
- **Containerization**: Docker containers cho triển khai Cloud Run
- **LLM Integration**: Tích hợp API mô hình ngôn ngữ lớn
- **RESTful APIs**: Giao tiếp giữa các thành phần
- **Serverless Architecture**: Tự động scale, mô hình thanh toán theo sử dụng

---

## Nguyên Tắc Thiết Kế

### 1. Serverless-First
Kiến trúc tận dụng Google Cloud Run cho triển khai serverless, cung cấp:
- Tự động scale dựa trên nhu cầu
- Tối ưu chi phí (chỉ trả tiền cho việc sử dụng thực tế)
- Không cần quản lý server
- Tính khả dụng cao

### 2. Thiết Kế Module
Các thành phần được ghép nối lỏng lẻo:
- **Web Application**: Xử lý lớp presentation
- **Chatbot**: Điều phối business logic
- **LLM**: Cung cấp khả năng AI
- **Tools**: Các module chức năng có thể mở rộng
- **Storage**: Lớp lưu trữ dữ liệu

### 3. Khả Năng Mở Rộng
- Cloud Run tự động scale cả dịch vụ Chatbot và Tools
- Storage scale độc lập
- Dịch vụ LLM xử lý các request đồng thời

### 4. Khả Năng Mở Rộng Chức Năng
- Tools có thể được thêm hoặc sửa đổi độc lập
- Chức năng mới có thể được triển khai mà không ảnh hưởng đến dịch vụ Chatbot cốt lõi
- Kiến trúc module hỗ trợ thêm tính năng theo từng bước

---

## Lợi Ích

### Hiệu Năng
- **Độ Trễ Thấp**: Kiến trúc serverless với routing yêu cầu được tối ưu
- **Tự Động Scale**: Xử lý tự động các đợt tăng traffic
- **Phân Phối Địa Lý**: Có thể triển khai trên nhiều khu vực

### Hiệu Quả Chi Phí
- **Trả Tiền Theo Sử Dụng**: Không tính phí khi không hoạt động
- **Tối Ưu Tài Nguyên**: Scale tự động tránh cấp phát quá mức
- **Dịch Vụ Quản Lý**: Giảm chi phí vận hành

### Độ Tin Cậy
- **Tính Khả Dụng Cao**: Được xây dựng trên hạ tầng đáng tin cậy của GCP
- **Chịu Lỗi**: Kiểm tra sức khỏe và khởi động lại tự động
- **Độ Bền Dữ Liệu**: Cloud Storage cung cấp độ bền 99.999999999%

### Khả Năng Bảo Trì
- **Triển Khai Container**: Môi trường nhất quán
- **Scale Độc Lập**: Mỗi thành phần scale độc lập
- **Phân Tách Rõ Ràng**: Dễ dàng cập nhật từng thành phần riêng biệt

---

## Các Vấn Đề Bảo Mật

### Xác Thực & Phân Quyền
- Triển khai xác thực phù hợp cho người dùng Web Application
- Sử dụng Cloud IAM cho xác thực giữa các dịch vụ
- Bảo mật API endpoints với kiểm soát truy cập phù hợp

### Bảo Vệ Dữ Liệu
- Mã hóa dữ liệu khi lưu trữ trên Cloud Storage
- Sử dụng HTTPS/TLS cho tất cả dữ liệu truyền đi
- Triển khai chính sách lưu giữ và xóa dữ liệu phù hợp

### Bảo Mật Mạng
- Cấu hình VPC và firewall rules phù hợp
- Sử dụng các tính năng bảo mật tích hợp của Cloud Run
- Triển khai giới hạn tốc độ và bảo vệ DDoS

---

## Chiến Lược Triển Khai

### Tích Hợp Liên Tục/Triển Khai Liên Tục (CI/CD)
1. Đẩy thay đổi code lên repository
2. Chạy các bài test tự động
3. Build container images
4. Triển khai lên Cloud Run (với rollout từng bước)
5. Kiểm tra sức khỏe và giám sát

### Quản Lý Môi Trường
- **Development**: Môi trường phát triển và test
- **Staging**: Xác thực trước khi đưa lên production
- **Production**: Môi trường người dùng thực tế

---

## Giám Sát & Khả Năng Quan Sát

### Logging
- Logging tự động của Cloud Run
- Logging cấp ứng dụng để debug
- Audit logs cho bảo mật và tuân thủ

### Metrics
- Độ trễ và throughput của request
- Tỷ lệ và loại lỗi
- Sử dụng tài nguyên (CPU, memory)
- Thống kê gọi công cụ
- Mô hình sử dụng storage

### Cảnh Báo
- Ngưỡng tỷ lệ lỗi
- Cảnh báo suy giảm độ trễ
- Cảnh báo hạn mức storage
- Phát hiện bất thường về chi phí

---

## Cải Tiến Trong Tương Lai

### Các Cải Tiến Tiềm Năng
1. **Hỗ Trợ Đa Phương Thức**: Thêm hỗ trợ cho hình ảnh, giọng nói và video
2. **RAG Nâng Cao**: Triển khai Retrieval-Augmented Generation để có ngữ cảnh tốt hơn
3. **Phân Tích Hội Thoại**: Phân tích sâu về tương tác người dùng
4. **Hỗ Trợ Đa Ngôn Ngữ**: Mở rộng để hỗ trợ nhiều ngôn ngữ
5. **Hub Tích Hợp**: Kết nối với nhiều dịch vụ và API bên ngoài hơn
6. **Edge Caching**: Triển khai lớp caching cho dữ liệu truy cập thường xuyên
7. **Framework A/B Testing**: Test các mô hình LLM và chiến lược prompting khác nhau

### Lộ Trình Mở Rộng
- Triển khai database cho dữ liệu có cấu trúc (Cloud SQL hoặc Firestore)
- Thêm lớp caching (Cloud Memorystore)
- Triển khai message queue cho xử lý bất đồng bộ (Cloud Pub/Sub)
- Triển khai trên nhiều khu vực để có sẵn toàn cầu

---

## Kết Luận

Kiến trúc này cung cấp một giải pháp mạnh mẽ, có khả năng mở rộng và hiệu quả về chi phí để xây dựng hệ thống chatbot thông minh trên Google Cloud Platform. Bằng cách tận dụng công nghệ serverless, các dịch vụ được quản lý và khả năng AI hiện đại, hệ thống có thể xử lý các tải thay đổi trong khi duy trì hiệu năng cao và độ tin cậy.

Thiết kế module cho phép mở rộng và bảo trì dễ dàng, trong khi cách tiếp cận cloud-native đảm bảo khả năng mở rộng và tối ưu chi phí. Khi hệ thống phát triển, kiến trúc có thể được nâng cao với các tính năng và khả năng bổ sung trong khi vẫn duy trì các nguyên tắc cốt lõi về tính đơn giản, khả năng mở rộng và khả năng bảo trì.
