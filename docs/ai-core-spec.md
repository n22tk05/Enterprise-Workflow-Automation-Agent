# Đặc tả Kỹ thuật - Phân hệ Agentic Core (Lõi AI)

**Vị trí thư mục:** `packages/agentic-core`
**Ngôn ngữ/Framework:** Python, LangChain, LangGraph

Bản đặc tả này đóng vai trò thiết kế chi tiết (Spec-driven) để định hướng việc xây dựng Giai đoạn 1 của dự án Enterprise Workflow Automation Agent. Giai đoạn này tập trung vào việc tạo ra vòng lặp tự chủ (Autonomous Loop) có khả năng hiểu ngôn ngữ, đưa ra quyết định, gọi công cụ giả lập và kết thúc quy trình.

---

## 1. Mục tiêu Phân hệ

- **Tự động phân tích:** Nhận tin nhắn đầu vào từ hệ thống, phân tích ý định người dùng.
- **Ra quyết định (Reasoning):** Tự động quyết định xem có cần gọi hệ thống bên ngoài để thu thập thông tin hoặc thực thi lệnh hay không.
- **Thực thi (Action):** Chạy các hàm tương ứng (Tools).
- **Quản lý trạng thái (State):** Duy trì và cập nhật bộ nhớ của toàn bộ cuộc hội thoại và tiến trình công việc.

---

## 2. Cấu trúc Thư mục Agentic Core

Cấu trúc nội bộ của `packages/agentic-core` sẽ được phân bổ như sau:

```text
packages/agentic-core/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── workflow.py         # Định nghĩa Graph (Nodes, Edges)
│   ├── state/
│   │   ├── __init__.py
│   │   └── graph_state.py      # Cấu trúc dữ liệu "Cuốn sổ tay" của Agent
│   ├── guardrails/
│   │   ├── __init__.py
│   │   └── filters.py          # Logic đánh giá tính hợp lệ, phát hiện rủi ro (Phase sau)
│   └── tools/
│       ├── __init__.py
│       └── mock_tools.py       # Khai báo các function giả lập (Tool Calling)
├── main.py                     # File entry-point để test trên terminal
├── requirements.txt            # Quản lý dependencies (langchain, langgraph,...)
└── .env                        # Chứa OPENAI_API_KEY hoặc GEMINI_API_KEY
```

---

## 3. Kiến trúc Đồ thị (Graph Architecture)

Hệ thống được xây dựng dưới dạng một **State Machine** (Máy trạng thái) thông qua `langgraph`.

### 3.1. Cấu trúc State (Trạng thái)
State đóng vai trò là mạch máu của Graph.
- **Dữ liệu chính:** Danh sách các thông điệp `messages` (HumanMessage, AIMessage, ToolMessage).
- **Biến phụ trợ (Tương lai):** `pending_approval` (Cờ chờ duyệt), `user_context` (Thông tin phân quyền).

### 3.2. Cấu trúc Trạm (Nodes)
Hệ thống sử dụng 2 node cốt lõi:
- **`agent_node`:** Khởi tạo mô hình LLM (như GPT-4 hoặc Gemini Pro). Được "nhồi" sẵn danh sách các Tools. Nhận đầu vào là State hiện tại và trả ra một tin nhắn mới (có thể là câu trả lời text hoặc một lệnh `tool_call`).
- **`action_node`:** Đứng ra đón các lệnh `tool_call` từ LLM, tự động mapping với hàm Python tương ứng, chạy hàm và trả kết quả vào State.

### 3.3. Cấu trúc Luồng (Edges & Routing)
- **Điểm bắt đầu (START) ->** `agent_node`
- **Từ `agent_node` rẽ nhánh (Conditional Edge):**
  - Nếu AI trả về `tool_calls` -> chuyển sang `action_node`.
  - Nếu AI không trả về `tool_calls` (đã có câu trả lời cuối cùng) -> kết thúc luồng (END).
- **Từ `action_node` ->** Vòng lại `agent_node` để AI tổng hợp kết quả.

---

## 4. Các Công cụ Giả lập (Mock Tools)

Trong Giai đoạn 1, Agentic Core sẽ làm việc với các hệ thống ERP/CRM giả lập thông qua Python Decorator `@tool`.

Các tools ban đầu cần xây dựng:
1. `check_leave_balance(user_id)`: Kiểm tra ngày phép. (Trả về số cố định để test).
2. `create_leave_request(user_id, days, reason)`: Tạo đơn nghỉ. (Trả về mã đơn giả định).
3. `get_employee_info(email)`: Trích xuất thông tin nhân sự.

*Yêu cầu kỹ thuật:* Mọi tool bắt buộc phải có phần `docstring` cực kỳ rõ ràng vì LLM dựa vào đoạn text đó để hiểu khi nào nên dùng tool này.

---

## 5. Quy trình Kiểm thử (Test Cases)

File `main.py` sẽ thực thi các kịch bản test sau trực tiếp qua Terminal:

- **Test Case 1 (Single Action):** 
  - *Đầu vào:* "Kiểm tra phép của tôi"
  - *Kỳ vọng:* Đi qua `agent_node` -> gọi `check_leave_balance` -> quay lại `agent_node` -> trả lời.
- **Test Case 2 (Multi-step Action):**
  - *Đầu vào:* "Kiểm tra phép của tôi, nếu còn đủ thì tạo cho tôi đơn nghỉ 3 ngày đi du lịch."
  - *Kỳ vọng:* Gọi `check_leave_balance` -> kiểm tra đủ điều kiện -> gọi tiếp `create_leave_request` -> kết luận hoàn thành.
- **Test Case 3 (Edge Case):**
  - *Đầu vào:* "Thời tiết hôm nay thế nào?"
  - *Kỳ vọng:* AI trả lời không có thẩm quyền hoặc không cần gọi tool nào, kết thúc luồng ngay sau vòng đầu tiên.

---

## 6. Tiêu chí Chấp nhận (Definition of Done - Giai đoạn 1)

1. Môi trường Python được thiết lập không có lỗi dependency.
2. File `workflow.py` biên dịch (compile) thành công Graph mà không báo lỗi vòng lặp vô hạn.
3. Chạy lệnh `python main.py`, AI phản hồi chính xác kết quả mô phỏng, ghi rõ quá trình chạy các hàm trong terminal.
4. (Tùy chọn) Stream được tin nhắn của AI thành từng token (Streaming) để tăng trải nghiệm.
