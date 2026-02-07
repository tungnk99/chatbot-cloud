# Checklist Dự Án – Chatbot Cloud

Đối chiếu theo **AGENT.md** và **docs/** để biết phần đã có và còn thiếu.

---

## Đã có (Done)

| Hạng mục | Chi tiết |
|----------|----------|
| **Cấu trúc** | `backend/chatbot`, `backend/tools`, `frontend`, `infrastructure/terraform`, `docs/` |
| **Backend Chatbot** | FastAPI: `/api/chat`, `/api/sessions`, `/api/sessions/{id}/messages`, `/health`; LLM (OpenAI) + Tools client; Storage (local + GCS) |
| **Backend Tools** | FastAPI: `/tools/interest`, `/tools/savings-rate`, `/health`, `/ready` |
| **Frontend** | Streamlit, gọi Chatbot API, session, lịch sử |
| **Docker** | Dockerfile từng service: python:3.11-slim, non-root, HEALTHCHECK, port 8080 |
| **Terraform** | APIs, GCS bucket, Secret Manager, Artifact Registry, IAM, 3 Cloud Run services |
| **Cloud Build** | `cloudbuild.yaml` build + push 3 images |
| **Tài liệu** | README (root + từng service), AGENT.md, CONTRIBUTING.md, docs (architecture, api, database, prd) |
| **Bảo mật** | Secret qua env/Secret Manager; Pydantic validate input; không commit secret (.gitignore) |
| **API** | RESTful, JSON, mã trạng thái đúng; health check |

---

## Đã bổ sung (theo AGENT.md)

| Hạng mục | Trạng thái |
|----------|------------|
| **Testing** | ✅ `backend/tools/tests/unit/`, `backend/chatbot/tests/unit/`; pytest; chạy: `cd backend/tools && pytest tests/`, `cd backend/chatbot && pytest tests/` |
| **CI/CD** | ✅ `.github/workflows/test.yml`: test Tools + Chatbot, lint (Black, isort) |
| **CORS** | ✅ Chatbot: CORSMiddleware, `cors_origins` từ env (mặc định localhost:8501) |
| **Rate limiting** | ✅ Chatbot: `/api/chat` giới hạn theo IP, `rate_limit_per_minute` (mặc định 60; 0 = tắt) |
| **Format/Lint** | ✅ `pyproject.toml`: pytest, Black, isort config |

## Còn có thể bổ sung (tùy chọn)

| Hạng mục | Yêu cầu (AGENT/docs) | Ưu tiên |
|----------|------------------------|---------|
| **Coverage ≥ 80%** | pytest-cov, báo cáo coverage trong CI | Trung bình |
| **Structured logging** | Log dạng JSON, request_id, latency_ms; không log message/token | Thấp |
| **Response format** | Chuẩn: `status` (success/error), `data` hoặc `error` – API hiện trả trực tiếp data | Thấp (demo có thể giữ) |
| **Integration / e2e** | Test gọi thật LLM/Tools (hoặc mock đầy đủ) | Thấp |

---

## Ghi chú

- **Demo**: Phần "Đã có" đủ để chạy end-to-end (local + GCP Terraform). Phần "Còn thiếu" nên làm để đạt chuẩn AGENT (test, CI, CORS, rate limit).
- **Production**: Nên bổ sung đủ test, CI/CD, CORS, rate limit, logging có cấu trúc, và (tùy chọn) response format thống nhất.

*Cập nhật: theo AGENT.md và docs tháng 2/2026.*
