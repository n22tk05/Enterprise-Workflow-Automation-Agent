# Enterprise Workflow Automation Agent

Nền tảng Tự động hóa Quy trình Nghiệp vụ Doanh nghiệp dựa trên kiến trúc AI Agentic Workflow. Hệ thống cho phép tự động hóa các quy trình nội bộ phức tạp (như tạo đơn nghỉ phép, tra cứu thông tin) thông qua giao tiếp bằng ngôn ngữ tự nhiên, kết hợp cơ chế kiểm soát an toàn duyệt bởi con người (Human-in-the-loop).

## Kiến trúc Dự án (Monorepo)

Dự án được xây dựng theo kiến trúc Monorepo, chia tách rõ ràng các phân hệ:

- `apps/web`: Giao diện người dùng (Chat Interface) và Admin Dashboard (React/Next.js) - *Sắp triển khai*
- `apps/api-server`: Backend xử lý nghiệp vụ, DB, phân quyền (Node.js/Python) - *Sắp triển khai*
- `packages/agentic-core`: **(Đã hoàn thành Phase 1)** Lõi AI điều phối quy trình bằng Python (LangGraph).
- `packages/integrations`: Connectors giao tiếp với các hệ thống ngoài (ERP, CRM).

## Giai đoạn 1: Agentic Core (Lõi AI)

Tập trung vào việc xây dựng "Bộ não AI" với vòng lặp ReAct, cho phép AI hiểu ngôn ngữ tự nhiên, tự động bóc tách tham số và gọi các công cụ giả lập (Mock Tools) phù hợp mà không cần can thiệp thủ công.

### Hướng dẫn Cài đặt và Chạy thử

**1. Khởi tạo môi trường ảo (Python)**
Mở terminal ở thư mục root và chạy:
```powershell
python -m venv .venv
# Kích hoạt venv trên Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

**2. Cài đặt thư viện**
```powershell
pip install langchain langchain-openai langgraph python-dotenv
```

**3. Cấu hình API Key**
- Truy cập vào thư mục `packages/agentic-core`.
- Đổi tên file `.env.example` thành `.env`.
- Điền `OPENAI_API_KEY` của bạn vào file `.env`.

**4. Chạy thử nghiệm AI Agent**
Chạy file script `main.py` để trò chuyện trực tiếp với Agent qua Terminal:
```powershell
cd packages/agentic-core
python main.py
```

## Tài liệu chi tiết (Docs)
- [Đặc tả Kỹ thuật Hệ thống (System Spec)](docs/spec.md)
- [Đặc tả Lõi AI (Agentic Core Spec)](docs/ai-core-spec.md)
