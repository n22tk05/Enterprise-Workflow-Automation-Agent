import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import uuid
# Load các biến môi trường (API Key) từ file .env
load_dotenv()

# Import cỗ máy AI (app) mà bạn đã vất vả lắp ráp
from src.agents.work_flow import app

def run_chat():
    print("===========================================================")
    print("🤖 ENTERPRISE AGENT ĐÃ SẴN SÀNG (Gõ 'quit' hoặc 'q' để thoát)")
    print("===========================================================")
    # Tạo MỘT thread_id duy nhất cho suốt phiên chat để AI nhớ ngữ cảnh
    chat_session_id = str(uuid.uuid4())[:255]
    config = {"configurable": {"thread_id": chat_session_id}}
    
    while True:
        user_input = input("\n👤 Bạn: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Tạm biệt!")
            break
            
        # Gói tin nhắn của người dùng vào chuẩn của LangChain
        inputs = {"messages": [HumanMessage(content=user_input)]}
        print("\n[HỆ THỐNG] ⏳ AI Đang suy nghĩ và xử lý...\n")
        
        # Hàm stream() sẽ chạy đồ thị và nhả kết quả sau mỗi Trạm (Node)
        for output in app.stream(inputs, stream_mode="values", config=config):
            last_msg = output["messages"][-1]
            
            # Nếu tin nhắn trả về là của AI và có chứa nội dung chữ (không phải lệnh gọi tool)
            if last_msg.type == "ai" and last_msg.content:
                print(f"🤖 AI: {last_msg.content}")

if __name__ == "__main__":
    # Kiểm tra xem bạn đã cấu hình API Key chưa trước khi cho phép chạy
    if not os.environ.get("GROQ_API_KEY"):
        print("❌ LỖI: Chưa tìm thấy khóa GROQ_API_KEY!")
        print("💡 Hướng dẫn sửa: Hãy tạo một file tên là '.env' nằm cùng thư mục với file main.py")
        print("Sau đó dán dòng này vào: GROQ_API_KEY=gsk_xxxxx (Thay bằng key của bạn)")
    else:
        run_chat()
