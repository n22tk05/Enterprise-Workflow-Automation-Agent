import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load các biến môi trường (API Key) từ file .env
load_dotenv()

# Import cỗ máy AI (app) mà bạn đã vất vả lắp ráp
from src.agents.work_flow import app

def run_chat():
    print("===========================================================")
    print("🤖 ENTERPRISE AGENT ĐÃ SẴN SÀNG (Gõ 'quit' hoặc 'q' để thoát)")
    print("===========================================================")
    
    while True:
        user_input = input("\n👤 Bạn: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Tạm biệt!")
            break
            
        # Gói tin nhắn của người dùng vào chuẩn của LangChain
        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        print("\n[HỆ THỐNG] ⏳ AI Đang suy nghĩ và xử lý...\n")
        
        # Hàm stream() sẽ chạy đồ thị và nhả kết quả sau mỗi Trạm (Node)
        for output in app.stream(inputs, stream_mode="values"):
            last_msg = output["messages"][-1]
            
            # Nếu tin nhắn trả về là của AI và có chứa nội dung chữ (không phải lệnh gọi tool)
            if last_msg.type == "ai" and last_message.content:
                print(f"🤖 AI: {last_msg.content}")

if __name__ == "__main__":
    # Kiểm tra xem bạn đã cấu hình API Key chưa trước khi cho phép chạy
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ LỖI: Chưa tìm thấy khóa OPENAI_API_KEY!")
        print("💡 Hướng dẫn sửa: Hãy tạo một file tên là '.env' nằm cùng thư mục với file main.py")
        print("Sau đó dán dòng này vào: OPENAI_API_KEY=sk-xxxxxxx (Thay xxxxx bằng key của bạn)")
    else:
        run_chat()
