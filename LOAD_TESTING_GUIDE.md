# 🦗 Load Testing với Locust - Chứng Minh Auto-scaling

## 📌 MỤC LỤC

1. [Giới Thiệu](#giới-thiệu)
2. [Quick Start](#quick-start)
3. [Cài Đặt](#cài-đặt)
4. [Chạy Tests](#chạy-tests)
5. [Thu Thập Evidence](#thu-thập-evidence)
6. [Phân Tích Kết Quả](#phân-tích-kết-quả)
7. [Demo Script](#demo-script)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 GIỚI THIỆU

Guide này hướng dẫn sử dụng **Locust** để:
- ✅ Load test hệ thống với giao diện web trực quan
- ✅ Chứng minh khả năng **auto-scaling** của Cloud Run
- ✅ Thu thập evidence (metrics, screenshots, reports)
- ✅ Demo live cho presentation

### Tại Sao Dùng Locust?

| Ưu Điểm | Chi Tiết |
|---------|----------|
| 🎨 **Giao diện đẹp** | Web UI real-time với charts tự động |
| 📊 **Graphs tích hợp** | Response time, RPS, failures |
| 🎛️ **Dynamic control** | Điều chỉnh số users on-the-fly |
| 📄 **HTML reports** | Export reports đẹp với graphs |
| 👀 **Live monitoring** | Xem metrics real-time |
| 📸 **Demo friendly** | Hoàn hảo cho presentation |

### Cấu Hình Auto-scaling

```hcl
# Cloud Run Configuration
min_instances = 0  # Scale-to-zero
max_instances = 10
cpu = 1 vCPU
memory = 512Mi
```

---

## 🚀 QUICK START

### 3 Bước Nhanh

```bash
# 1. Cài đặt
pip install -r tests/load/requirements.txt

# 2. Chạy Locust
./run-locust-interactive.sh

# 3. Mở browser
http://localhost:8089
```

### 2 Cách Chạy Tests

| Cách | Thời Gian | Sử Dụng |
|------|-----------|---------|
| **Interactive** | 15-20 phút | ⭐ Demo live, presentation |
| **Automated** | 20-25 phút | Thu thập evidence đầy đủ |

---

## 📦 CÀI ĐẶT

### Prerequisites

```bash
# Python 3.8+
python3 --version

# Pip
pip --version

# Google Cloud CLI (optional, cho metrics)
gcloud --version
```

### Install Dependencies

```bash
cd /home/tungnk/Desktop/Masters-HUST/Cloud\ Computing/BTL/chatbot-cloud

# Install từ requirements
pip install -r tests/load/requirements.txt

# Hoặc install trực tiếp
pip install locust==2.32.4 httpx==0.28.1
```

### Verify Installation

```bash
locust --version
# Output: locust 2.32.4
```

---

## 🦗 CHẠY TESTS

### CÁCH 1: Interactive Mode (Recommended)

#### Khởi Động Locust Web UI

```bash
# Set service URL (đã có sẵn trong script)
export CHATBOT_URL="https://chatbot-api-hbfjjbwmsa-as.a.run.app"

# Chạy script
./run-locust-interactive.sh
```

Output:
```
🦗 Locust Interactive Load Testing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target URL:  https://chatbot-api-hbfjjbwmsa-as.a.run.app
Web UI URL:  http://localhost:8089

Starting Locust...
```

#### Mở Web UI

```bash
# Tự động mở trong browser
xdg-open http://localhost:8089

# Hoặc mở manual
firefox http://localhost:8089
```

#### Chuẩn Bị 2 Tabs

**Tab 1**: Locust UI
- http://localhost:8089

**Tab 2**: GCP Console Metrics
- https://console.cloud.google.com/run/detail/asia-southeast1/chatbot-api/metrics

#### Kịch Bản Test

##### Test 1: Baseline (1-2 phút)
```
Purpose: Wake up service, verify connectivity
Settings:
  - Number of users: 5
  - Spawn rate: 1 user/second
  - Click "Start swarming"

Expected:
  - GCP Console: Instances 0 → 1
  - Locust: Success rate >95%
  - Response time: <3s
```

##### Test 2: Light Load (2-3 phút)
```
Purpose: Light traffic, basic scaling
Settings:
  - Stop previous test
  - Number of users: 10
  - Spawn rate: 2 users/second
  - Start swarming

Expected:
  - GCP Console: 1-2 instances
  - Locust: 3-5 RPS
  - Success rate: >95%

📸 CHỤP SCREENSHOTS:
  - Locust Statistics table
  - Locust Charts tab
  - GCP Instance count
```

##### Test 3: Medium Load (3-4 phút)
```
Purpose: Moderate scaling
Settings:
  - Stop test
  - Wait 1 minute (scale-down)
  - Number of users: 50
  - Spawn rate: 5 users/second
  - Start swarming

Expected:
  - GCP Console: 3-5 instances
  - Locust: 15-25 RPS
  - Success rate: >90%
  - Response time: <5s

📸 CHỤP SCREENSHOTS:
  - GCP Instance count tăng
  - Locust Charts showing load increase
```

##### Test 4: Heavy Load (3-4 phút)
```
Purpose: Near-max capacity
Settings:
  - Stop test
  - Wait 1 minute
  - Number of users: 100
  - Spawn rate: 10 users/second
  - Start swarming

Expected:
  - GCP Console: 7-10 instances (max)
  - Locust: 30-50 RPS
  - Success rate: >85%
  - Response time: <8s

📸 CHỤP SCREENSHOTS:
  - GCP Instance count at max
  - Locust performance under load
```

##### Test 5: Spike Test (2-3 phút)
```
Purpose: Rapid scaling test
Settings:
  - Stop test
  - Number of users: 200
  - Spawn rate: 50 users/second (RAPID!)
  - Start swarming

Expected:
  - GCP Console: Rapid scale to 8-10 instances
  - Locust: 40-70 RPS
  - Success rate: >80%
  - Some latency increase acceptable

📸 CHỤP SCREENSHOTS:
  - Rapid scaling in GCP
  - Spike handling in Locust
```

##### Test 6: Scale-down (5-10 phút)
```
Purpose: Verify auto scale-down
Settings:
  - Stop all tests
  - Watch GCP Console

Expected:
  - GCP Console: Instances gradually decrease
  - After 5-10 minutes: Back to 0 instances
  - Demonstrates scale-to-zero

📸 CHỤP SCREENSHOTS:
  - Scale-down progress
  - Final state: 0 instances
```

#### Export Reports

Sau mỗi test phase:
1. Locust UI → Tab **"Download Data"**
2. Click **"Download Report"**
3. Save HTML file: `report-light.html`, `report-medium.html`, etc.

#### Stop Locust

```bash
# Press Ctrl+C trong terminal
^C
```

---

### CÁCH 2: Automated Mode

#### Chạy Tất Cả Tests Tự Động

```bash
# Chạy script automated
./run-locust-tests.sh
```

Script sẽ:
- ✅ Chạy 4 test profiles (light, medium, heavy, spike)
- ✅ Thu thập GCP metrics sau mỗi test
- ✅ Wait cooldown giữa các tests
- ✅ Tạo HTML reports tự động
- ✅ Export metrics JSON
- ✅ Generate summary README

**Thời gian**: ~20-25 phút

**Output**: `evidence/locust-YYYYMMDD_HHMMSS/`

#### Xem Kết Quả

```bash
# Navigate to evidence folder
cd evidence/locust-*/

# List all reports
ls -lh locust-reports/

# Open HTML reports
xdg-open locust-reports/01-light.html
xdg-open locust-reports/02-medium.html
xdg-open locust-reports/03-heavy.html
xdg-open locust-reports/04-spike.html

# View metrics
ls -lh metrics/

# Read summary
cat README.md
```

---

## 📊 THU THẬP EVIDENCE

### 1. Locust Reports

#### HTML Reports
Mỗi report bao gồm:
- **Statistics Table**: RPS, response times, success rate
- **Charts**: Response time distribution, RPS over time
- **Failures**: Error details (nếu có)
- **Download Data**: Export CSV

#### CSV Files
- `*_stats.csv`: Statistics chi tiết
- `*_failures.csv`: Failures log
- `*_stats_history.csv`: Timeline data

### 2. Screenshots từ Locust UI

#### Tab Statistics
- [ ] Request count và success rate
- [ ] Median response time
- [ ] 95th percentile latency
- [ ] Requests per second
- [ ] Failures count

#### Tab Charts
- [ ] Total Requests per Second (timeline)
- [ ] Response Times (timeline)
- [ ] Number of Users (ramp-up pattern)

#### Tab Failures (nếu có)
- [ ] Error types và counts
- [ ] Failed requests details

### 3. Screenshots từ GCP Console

#### Metrics Tab
Navigate to: **Cloud Run → chatbot-api → METRICS**

Chụp screenshots:
- [ ] **Container instance count** (graph chính - toàn bộ timeline)
- [ ] Instance count tại mỗi load level (0→1→5→10→0)
- [ ] **Request count** over time
- [ ] **Request latency** percentiles (P50, P95, P99)
- [ ] **CPU utilization**
- [ ] **Memory utilization**

#### Logs Tab
Navigate to: **Cloud Run → chatbot-api → LOGS**

Filter logs:
```
resource.type="cloud_run_revision"
"Starting" OR "Shutting down"
```

Chụp screenshots:
- [ ] Instance start events
- [ ] Instance stop events
- [ ] Scaling logs timeline

#### Service Details
Navigate to: **Cloud Run → chatbot-api**

Chụp screenshot:
- [ ] Service configuration showing:
  - Min instances: 0
  - Max instances: 10
  - CPU: 1 vCPU
  - Memory: 512Mi

### 4. Export Metrics từ GCP CLI

```bash
# Create evidence folder
mkdir -p evidence/manual-$(date +%Y%m%d_%H%M%S)
cd evidence/manual-*

# Instance count metrics
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/container/instance_count" AND resource.labels.service_name="chatbot-api"' \
  --format=json \
  --freshness=1h \
  > instance-count.json

# Request count
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count" AND resource.labels.service_name="chatbot-api"' \
  --format=json \
  --freshness=1h \
  > request-count.json

# Request latency
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_latencies" AND resource.labels.service_name="chatbot-api"' \
  --format=json \
  --freshness=1h \
  > request-latency.json

# CPU utilization
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/container/cpu/utilizations" AND resource.labels.service_name="chatbot-api"' \
  --format=json \
  --freshness=1h \
  > cpu-utilization.json

# Scaling logs
gcloud logging read \
  'resource.type="cloud_run_revision" 
   AND resource.labels.service_name="chatbot-api"
   AND ("Starting" OR "Shutting down")' \
  --limit=200 \
  --format=json \
  --freshness=1h \
  > scaling-logs.json
```

### 5. Evidence Checklist

#### Test Results
- [ ] Locust HTML reports (4 files: light, medium, heavy, spike)
- [ ] CSV statistics files
- [ ] CSV failures files (nếu có)
- [ ] Test logs

#### Screenshots - Locust
- [ ] Statistics table cho mỗi test
- [ ] Charts: Response time over time
- [ ] Charts: Total RPS over time
- [ ] Charts: Number of users ramp-up
- [ ] Download data section

#### Screenshots - GCP Console
- [ ] Instance count graph (full timeline)
- [ ] Instance count at baseline (0)
- [ ] Instance count at light load (1-2)
- [ ] Instance count at medium load (3-5)
- [ ] Instance count at heavy load (7-10)
- [ ] Instance count after scale-down (0)
- [ ] Request latency percentiles
- [ ] Service configuration

#### Metrics Data
- [ ] instance-count.json
- [ ] request-count.json
- [ ] request-latency.json
- [ ] cpu-utilization.json
- [ ] scaling-logs.json

---

## 📈 PHÂN TÍCH KẾT QUẢ

### Reading Locust HTML Reports

#### 1. Statistics Section

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| **Success Rate** | >95% | >85% | <85% |
| **Median Response** | <3s | <5s | >5s |
| **95th Percentile** | <8s | <12s | >12s |
| **Requests/sec** | Increasing | Stable | Decreasing |

#### 2. Charts Analysis

**Response Time Chart**:
- ✅ Stable horizontal line = good performance
- ⚠️ Gradual increase = approaching limits
- ❌ Spikes during scaling = normal, should stabilize

**Total RPS Chart**:
- ✅ Increases with users = good scaling
- ⚠️ Plateaus = hitting capacity
- ❌ Decreases = system overload

**Number of Users Chart**:
- Verify ramp-up pattern matches spawn rate
- Smooth curve = healthy spawn rate

### Correlating với GCP Metrics

#### Timeline Correlation

| Time | Locust Users | RPS | GCP Instances | Observation |
|------|--------------|-----|---------------|-------------|
| 0:00 | 0 | 0 | 0 | Baseline: scale-to-zero |
| 0:30 | 5 | 2 | 1 | Wake up from 0 |
| 2:00 | 10 | 5 | 1-2 | Light load |
| 5:00 | 50 | 20 | 3-5 | Medium scaling |
| 8:00 | 100 | 45 | 7-10 | Heavy load |
| 11:00 | 200 | 60 | 10 | Max instances |
| 13:00 | 0 | 0 | 5 | Scale-down started |
| 18:00 | 0 | 0 | 0 | Back to zero |

### Expected Results

#### Test Performance

| Test | Users | Total Requests | Success Rate | Avg Latency | P95 Latency | RPS | Instances |
|------|-------|----------------|--------------|-------------|-------------|-----|-----------|
| Light | 10 | ~100 | >95% | <3s | <5s | 3-5 | 1-2 |
| Medium | 50 | ~1000 | >90% | <4s | <8s | 15-25 | 3-5 |
| Heavy | 100 | ~2500 | >85% | <6s | <12s | 30-50 | 7-10 |
| Spike | 200 | ~1500 | >80% | <8s | <15s | 40-70 | 8-10 |

#### Auto-scaling Evidence

✅ **Scale-up Demonstrated**:
- Instance count tăng từ 0 → 1 → 3 → 5 → 10
- Tương ứng với load tăng
- Response time vẫn acceptable

✅ **Performance Under Load**:
- Success rate duy trì >85%
- Latency không tăng quá nhiều
- System handle được traffic

✅ **Elasticity**:
- Instances scale nhanh khi load tăng đột ngột
- Không có downtime during scaling

✅ **Scale-down Demonstrated**:
- Instance count giảm sau khi load giảm
- Return về 0 (min_instances)
- Cost optimization working

✅ **Scale-to-Zero**:
- Service start từ 0 instances
- Return về 0 khi idle
- Tiết kiệm chi phí

---

## 🎬 DEMO SCRIPT (CHO PRESENTATION)

### Preparation (5 phút trước)

```bash
# 1. Verify service đang idle
gcloud run services describe chatbot-api --region=asia-southeast1 | grep instance

# 2. Start Locust
./run-locust-interactive.sh

# 3. Open browsers
firefox http://localhost:8089 &
firefox https://console.cloud.google.com/run/detail/asia-southeast1/chatbot-api/metrics &

# 4. Arrange windows side-by-side
```

### Live Demo Timeline (10-12 phút)

#### 00:00 - 01:00 | Giới Thiệu
```
🎤 "Hôm nay tôi sẽ demo khả năng auto-scaling của hệ thống"

Show screens:
- Locust UI
- GCP Console: 0 instances (scale-to-zero)

🎤 "Hiện tại service đang ở 0 instances để tiết kiệm chi phí"
```

#### 01:00 - 03:00 | Baseline Test
```
Locust UI:
- Number of users: 5
- Spawn rate: 1
- Click "Start swarming"

🎤 "Khi có traffic, Cloud Run tự động tạo instance đầu tiên"

Show GCP Console:
- Instance count: 0 → 1
- Request count tăng

🎤 "Đây là scale-up từ zero. Service ready trong vài giây"
```

#### 03:00 - 06:00 | Medium Load
```
Locust UI:
- Stop test
- Number of users: 50
- Spawn rate: 5
- Start swarming

🎤 "Tăng lên 50 concurrent users"

Show GCP Console:
- Instance count: 1 → 3 → 5
- Graphs tăng

Show Locust Charts:
- RPS tăng
- Response time stable

🎤 "Hệ thống tự động scale lên 5 instances"
🎤 "Response time vẫn ổn định nhờ auto-scaling"
```

#### 06:00 - 09:00 | Heavy Load
```
Locust UI:
- Stop, wait 30s
- Number of users: 100
- Spawn rate: 10
- Start swarming

🎤 "Tăng lên 100 users để test near-max capacity"

Show GCP Console:
- Instance count: 5 → 8 → 10 (max)

Show Locust:
- Higher RPS
- Still acceptable response times

🎤 "Đạt max 10 instances như đã config"
🎤 "Success rate vẫn >85%, system handle tốt"
```

#### 09:00 - 12:00 | Scale-down
```
Locust UI:
- Stop test

🎤 "Bây giờ tôi stop test để xem scale-down"

Watch GCP Console:
- Instance count: 10 → 7 → 5 → 3 → 1 → 0

🎤 "Khi không còn traffic, instances tự động giảm"
🎤 "Sau vài phút, về lại 0 instances"
🎤 "Đây là cost optimization - chỉ trả tiền khi có traffic"
```

### Key Messages cho Demo

```
✅ "Scale-to-zero: Start từ 0, tiết kiệm chi phí khi idle"

✅ "Auto scale-up: Tự động tạo instances khi có traffic"

✅ "Proportional scaling: Instances tăng theo load (1→5→10)"

✅ "Performance maintained: Response time stable nhờ scaling"

✅ "Elasticity: Rapid response to demand changes"

✅ "Auto scale-down: Giảm instances khi idle, optimize costs"

✅ "Cloud native benefits: Không cần manual intervention"
```

### Talking Points

**Scale-to-zero**:
> "Khi không có traffic, service ở 0 instances. Chúng ta không mất tiền cho resources không dùng."

**Scale-up**:
> "Khi có request đầu tiên, Cloud Run tự động tạo instance. Không cần config thêm gì."

**Proportional**:
> "Load tăng, instances tăng. Từ 1 lên 5 lên 10. Hoàn toàn tự động."

**Performance**:
> "Nhìn vào graph Locust, response time vẫn ổn định dù load tăng. Đó là nhờ auto-scaling."

**Cost**:
> "Sau khi test xong, instances tự động giảm về 0. Đây là optimization - chỉ trả cho những gì dùng."

---

## 🐛 TROUBLESHOOTING

### Issue 1: Port 8089 đã được sử dụng

```bash
# Check process
lsof -i :8089

# Kill old process
pkill -f locust

# Hoặc dùng port khác
LOCUST_PORT=8090 ./run-locust-interactive.sh
```

### Issue 2: Locust không start

```bash
# Check installation
locust --version

# Reinstall
pip uninstall locust
pip install locust==2.32.4

# Check Python version
python3 --version  # Need 3.8+
```

### Issue 3: High failure rate trong tests

**Nguyên nhân**:
- Cold start (service đang ở 0 instances)
- Rate limiting
- Service errors

**Giải pháp**:
```bash
# 1. Warm up service trước
# Start với baseline test (5 users) trước khi heavy test

# 2. Giảm spawn rate
# Thay vì 50 users/s, dùng 10 users/s

# 3. Check service logs
./view-logs.sh chatbot

# 4. Verify service health
curl https://chatbot-api-hbfjjbwmsa-as.a.run.app/health
```

### Issue 4: Không thấy scaling trong GCP Console

**Check configuration**:
```bash
# Verify max_instances
cd infrastructure/terraform
terraform show | grep max_instance

# Should show: max_instance_count = 10
```

**Check current state**:
```bash
# Get current instances
gcloud run services describe chatbot-api \
  --region=asia-southeast1 \
  --format='value(status.traffic[0].latestRevision)'

# Check quotas
gcloud compute project-info describe --project=$(gcloud config get-value project)
```

**Wait for metrics**:
- Metrics có thể delay 2-5 phút
- Refresh GCP Console (F5)
- Wait và check lại

### Issue 5: Service timeout

```bash
# Check timeout setting
gcloud run services describe chatbot-api \
  --region=asia-southeast1 \
  --format='value(spec.template.spec.timeoutSeconds)'

# Should be: 300s

# Check logs for actual errors
gcloud logging read \
  'resource.type="cloud_run_revision" 
   AND resource.labels.service_name="chatbot-api"
   AND severity>=ERROR' \
  --limit=20
```

### Issue 6: Cannot access GCP metrics

```bash
# Login to gcloud
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Test access
gcloud monitoring time-series list --limit=1
```

---

## 📚 REFERENCE

### Test Profiles Summary

| Profile | Users | Spawn Rate | Duration | Expected |
|---------|-------|------------|----------|----------|
| Baseline | 5 | 1/s | 1-2m | Wake up service |
| Light | 10 | 2/s | 2-3m | 1-2 instances |
| Medium | 50 | 5/s | 3-4m | 3-5 instances |
| Heavy | 100 | 10/s | 3-4m | 7-10 instances |
| Spike | 200 | 50/s | 2-3m | Rapid to max |

### Scripts Quick Reference

```bash
# Interactive mode (recommended)
./run-locust-interactive.sh

# Automated mode
./run-locust-tests.sh

# Manual Locust command
CHATBOT_URL="<URL>" locust \
  -f tests/load/locustfile.py \
  --host="<URL>" \
  --users=50 \
  --spawn-rate=5 \
  --run-time=3m \
  --headless \
  --html=report.html

# Check service
gcloud run services describe chatbot-api --region=asia-southeast1

# View logs
gcloud logging read 'resource.type="cloud_run_revision"' --limit=20

# Get instance count
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/container/instance_count"' \
  --format=json --freshness=5m
```

### Files Structure

```
chatbot-cloud/
├── run-locust-interactive.sh    # ⭐ Interactive mode
├── run-locust-tests.sh          # Automated mode
├── LOAD_TESTING_GUIDE.md        # ⭐ This file
├── tests/load/
│   ├── locustfile.py           # Test scenarios
│   ├── requirements.txt        # Dependencies
│   └── README.md               # Load tests overview
└── evidence/                    # Test results output
    └── locust-YYYYMMDD_HHMMSS/
        ├── locust-reports/     # HTML reports
        ├── metrics/            # GCP metrics JSON
        └── README.md           # Test summary
```

### Important URLs

- **Locust Docs**: https://docs.locust.io/
- **GCP Console**: https://console.cloud.google.com/run
- **Cloud Run Docs**: https://cloud.google.com/run/docs/configuring/max-instances

---

## ✅ CHECKLIST CUỐI CÙNG

### Trước Khi Demo

- [ ] Install dependencies: `pip install -r tests/load/requirements.txt`
- [ ] Verify service URL trong script
- [ ] Test chạy Locust: `./run-locust-interactive.sh`
- [ ] Verify GCP Console access
- [ ] Prepare 2 browser tabs (Locust + GCP)
- [ ] (Optional) Screen recording tool

### Trong Demo

- [ ] Chạy baseline test
- [ ] Chụp screenshot sau mỗi test
- [ ] Export Locust HTML reports
- [ ] Monitor GCP Console real-time
- [ ] Document observations

### Sau Demo

- [ ] Thu thập tất cả screenshots
- [ ] Export GCP metrics JSON
- [ ] Organize evidence folder
- [ ] Tạo summary report
- [ ] Review findings

---

## 🎉 SẴN SÀNG!

### Quick Start Command

```bash
./run-locust-interactive.sh
```

### Mở Browser

```
http://localhost:8089
```

### Start Testing! 🚀

**Good luck với presentation!** 🍀

---

**Last Updated**: 2026-02-10  
**Version**: 1.0  
**Author**: Cloud Computing BTL Team
