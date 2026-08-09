# Bản Đặc tả Kỹ thuật và Nghiệp vụ (Technical & Functional Specification)

**Chủ đề:** Nền tảng Tự động hóa Quy trình Nghiệp vụ Doanh nghiệp (Enterprise Workflow Automation Agent)

Bản đặc tả này đóng vai trò là tài liệu định hướng tổng quan cho toàn bộ dự án, xác định rõ phạm vi, cấu trúc hệ thống, luồng nghiệp vụ và các giá trị cốt lõi nhằm phục vụ cho việc phát triển sản phẩm cũng như trình bày trong hồ sơ năng lực (CV).

---

## 1. Giới thiệu và Mục tiêu Dự án (Project Overview & Objectives)

### 1.1. Tên dự án

**Enterprise Workflow Automation Agent**

### 1.2. Mục tiêu chính

Xây dựng một trợ lý ảo thông minh cấp độ doanh nghiệp (Enterprise Agent) có khả năng tự động hóa các quy trình nghiệp vụ phức tạp thông qua giao diện hội thoại ngôn ngữ tự nhiên, kết hợp khả năng:

- Tự lập kế hoạch (Planning).
- Gọi API hệ thống (Tool/API Calling).
- Quản lý trạng thái quy trình (State Management).
- Kiểm soát an toàn bằng cơ chế con người trong vòng lặp (Human-in-the-loop).

### 1.3. Đối tượng sử dụng

| Đối tượng | Vai trò |
|---|---|
| **Nhân viên nội bộ** | Tương tác với hệ thống qua khung chat để yêu cầu thực hiện các tác vụ công việc như tạo đơn, tra cứu thông tin, gửi báo cáo. |
| **Quản lý / Trưởng phòng** | Theo dõi tiến trình và phê duyệt các yêu cầu nhạy cảm thông qua Dashboard quản trị. |
| **Quản trị viên hệ thống (Admin)** | Giám sát nhật ký hoạt động (Audit Logs), cấu hình phân quyền và quản lý các kết nối hệ thống. |

---

## 2. Phạm vi Hệ thống (System Scope)

Hệ thống bao gồm **4 phân hệ kỹ thuật chính**:

```text
┌────────────────────────────────────────────────────────┐
│               PRESENTATION LAYER (Frontend)            │
│                                                        │
│       - Chat Interface (Giao diện ra lệnh AI)          │
│       - Admin Dashboard (Quản trị & Phê duyệt)         │
└───────────────────────────┬────────────────────────────┘
                            │
                  RESTful API / WebSockets
                            │
┌───────────────────────────▼────────────────────────────┐
│              AGENTIC ORCHESTRATION LAYER (Backend)     │
│                                                        │
│       - LLM Reasoning & Planning Engine                │
│       - State Management & Workflow Engine             │
│       - Guardrails & Safety Filters                    │
└───────────────────────────┬────────────────────────────┘
                            │
                     Function Calling
                            │
┌───────────────────────────▼────────────────────────────┐
│               INTEGRATION & DATA LAYER                 │
│                                                        │
│       - Tool/API Connectors (ERP, CRM, Database)       │
│       - Intelligent Document Processing (IDP/OCR)      │
│       - Vector Database (RAG cho tài liệu nội bộ)      │
└────────────────────────────────────────────────────────┘
```

### 2.1. Presentation Layer

Cung cấp giao diện tương tác trực tiếp với người dùng, bao gồm:

- **Chat Interface:** Giao diện hội thoại để người dùng ra lệnh cho Agent.
- **Admin Dashboard:** Giao diện quản trị, theo dõi workflow và xử lý các yêu cầu cần phê duyệt.

### 2.2. Agentic Orchestration Layer

Đóng vai trò là trung tâm điều phối của hệ thống:

- **LLM Reasoning & Planning Engine:** Phân tích yêu cầu và xây dựng kế hoạch thực hiện.
- **State Management & Workflow Engine:** Quản lý trạng thái và tiến trình của workflow.
- **Guardrails & Safety Filters:** Kiểm soát các hành động đầu vào, đầu ra và quyền thực thi.

### 2.3. Integration & Data Layer

Cung cấp khả năng kết nối với các hệ thống và nguồn dữ liệu bên ngoài:

- **Tool/API Connectors:** Kết nối với ERP, CRM, Database và các hệ thống nghiệp vụ khác.
- **Intelligent Document Processing (IDP/OCR):** Trích xuất và xử lý dữ liệu từ tài liệu.
- **Vector Database:** Lưu trữ dữ liệu phục vụ cơ chế RAG đối với tài liệu nội bộ.

---

## 3. Đặc tả Chức năng Chi tiết (Functional Requirements)

### A. Phân hệ Giao diện Hội thoại (Natural Language Interface)

Hệ thống phải cho phép người dùng:

- Nhập yêu cầu bằng ngôn ngữ tự nhiên.
- Hỗ trợ tiếng Việt và tiếng Anh.
- Theo dõi trạng thái xử lý của Agent theo thời gian thực.

**Ví dụ trạng thái:**

```text
Đang phân tích yêu cầu...
        ↓
Đang lập kế hoạch thực hiện...
        ↓
Đang gọi API kiểm tra dữ liệu...
        ↓
Đang xử lý kết quả...
        ↓
Hoàn thành
```

### B. Phân hệ Lõi AI & Điều phối Quy trình (Agentic Core)

#### B.1. Intent Recognition

Phân tích câu lệnh của người dùng để xác định chính xác mục đích nghiệp vụ (Business Intent).

**Ví dụ:**

> "Tạo đơn nghỉ phép 3 ngày từ thứ Hai."

**Agent xác định:**

- Intent: `CREATE_LEAVE_REQUEST`
- Duration: `3 days`
- Start Date: `Monday`

#### B.2. Task Decomposition

Tự động phân rã yêu cầu phức tạp thành các bước thực hiện tuần tự hoặc song song.

**Ví dụ:**

```text
User Request
     │
     ▼
Xác định nhân viên
     │
     ▼
Kiểm tra số ngày phép
     │
     ▼
Kiểm tra lịch làm việc
     │
     ▼
Tạo đơn nghỉ phép
     │
     ▼
Gửi yêu cầu phê duyệt
```

#### B.3. Tool Calling (Function Calling)

Agent tự động:

1. Xác định công cụ/API phù hợp.
2. Xác định tham số cần truyền.
3. Gọi API.
4. Nhận kết quả.
5. Sử dụng kết quả để thực hiện bước tiếp theo.

### C. Phân hệ Phê duyệt và Kiểm soát An toàn (Human-in-the-Loop & Guardrails)

#### C.1. Breakpoint / Suspend State

Agent tự động tạm dừng workflow khi gặp các tác vụ có mức độ rủi ro cao.

**Ví dụ:**

- Duyệt chi phí lớn.
- Thay đổi thông tin nhân sự.
- Xóa dữ liệu.
- Thực hiện giao dịch quan trọng.
- Thay đổi quyền truy cập.

**Workflow:**

```text
Agent
  │
  ▼
Phát hiện hành động nhạy cảm
  │
  ▼
SUSPEND
  │
  ▼
Gửi yêu cầu phê duyệt
  │
  ▼
Manager Dashboard
  │
  ├──► APPROVE ──► Tiếp tục Workflow
  │
  └──► REJECT  ──► Dừng Workflow
```

#### C.2. Approval Dashboard

Cung cấp giao diện cho quản lý:

- Xem yêu cầu.
- Xem ngữ cảnh thực thi.
- Xem các bước Agent đã thực hiện.
- Xem dữ liệu liên quan.
- Phê duyệt hoặc từ chối yêu cầu.

#### C.3. Guardrails

Bộ kiểm soát nhằm:

- Ngăn chặn các hành động vượt quyền.
- Kiểm tra dữ liệu đầu vào.
- Kiểm tra dữ liệu đầu ra.
- Hạn chế các hành động nguy hiểm.
- Giảm thiểu nguy cơ hallucination.
- Đảm bảo Agent chỉ sử dụng các công cụ được cấp quyền.

### D. Phân hệ Nhật ký và Lưu trữ (Audit Trail & State Persistence)

#### D.1. State Machine Persistence

Hệ thống phải lưu trữ trạng thái workflow để đảm bảo:

- Không mất tiến trình khi hệ thống khởi động lại.
- Có thể tiếp tục workflow sau khi bị tạm dừng.
- Hỗ trợ các workflow kéo dài nhiều ngày.
- Có khả năng khôi phục trạng thái trước đó.

#### D.2. Audit Trail

Hệ thống ghi lại toàn bộ lịch sử hoạt động của Agent.

**Luồng log:**

```text
Thought
   ↓
Action
   ↓
Observation
   ↓
Next Decision
   ↓
Action
   ↓
Observation
```

**Audit log phục vụ:**

- Kiểm tra hoạt động.
- Debugging.
- Phân tích lỗi.
- Theo dõi trách nhiệm.
- Minh bạch hóa quá trình vận hành.

---

## 4. Tiêu chuẩn Kỹ thuật và Công nghệ Dự kiến (Proposed Tech Stack)

### 4.1. Frontend

- React / Next.js
- Tailwind CSS

**Sử dụng để xây dựng:**

- Chat Interface.
- Admin Dashboard.
- Approval Dashboard.
- Workflow Monitoring.

### 4.2. Backend & API

**Có thể lựa chọn một trong các hướng:**

- Node.js + Express
- Node.js + NestJS
- Python + FastAPI

**Đảm nhiệm:**

- Business Logic.
- RESTful API.
- WebSocket.
- Authentication.
- Authorization.
- RBAC.
- Workflow Management.

### 4.3. AI Orchestration Framework

- LangGraph
- CrewAI

**Sử dụng để xây dựng:**

- Agent Workflow.
- State Graph.
- Task Decomposition.
- Tool Calling.
- Reasoning Loop.
- Human-in-the-loop.

### 4.4. Database & ORM

- MongoDB / PostgreSQL
- Prisma ORM

**Quản lý:**

- User.
- Role & Permission.
- Workflow.
- Workflow State.
- Transaction.
- Tool Execution.
- Approval Request.
- Audit Log.

### 4.5. Integration & AI Data Layer

- ERP APIs.
- CRM APIs.
- Internal Database.
- Document Processing.
- OCR.
- Vector Database.
- RAG cho tài liệu nội bộ.

---

## 5. Tiêu chí Đánh giá Thành công (Success Metrics)

### 5.1. Task Completion Rate

Đánh giá tỷ lệ Agent hoàn thành chính xác toàn bộ quy trình từ đầu đến cuối trên tập dữ liệu thử nghiệm.

**Mục tiêu:**

- Tối đa hóa tỷ lệ hoàn thành workflow chính xác mà không xảy ra lỗi logic.

### 5.2. Safety & Reliability

Hệ thống phải đảm bảo:

- 100% tác vụ được xác định là nhạy cảm phải đi qua bước Human-in-the-loop trước khi thực thi.

**Các cơ chế kiểm soát bao gồm:**

- Permission Check.
- Risk Classification.
- Approval Workflow.
- Guardrails.
- Audit Logging.

### 5.3. User Experience

Đánh giá dựa trên:

- Thời gian phản hồi của hệ thống.
- Tính trực quan của giao diện.
- Khả năng theo dõi tiến trình Agent.
- Tính rõ ràng của yêu cầu phê duyệt.
- Mức độ dễ sử dụng đối với nhân viên và quản lý.

> **Mục tiêu** là xây dựng một hệ thống có khả năng tự động hóa quy trình nghiệp vụ nhưng vẫn đảm bảo tính kiểm soát, minh bạch và an toàn trong môi trường doanh nghiệp.