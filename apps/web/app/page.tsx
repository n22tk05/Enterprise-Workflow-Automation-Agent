'use client';

import { useState, useRef, useEffect } from 'react';

// Định nghĩa kiểu dữ liệu cho tin nhắn
type Message = {
  id: string;
  sender: 'user' | 'ai';
  text: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { id: '1', sender: 'ai', text: 'Xin chào! Tôi là Trợ lý ảo Enterprise.\nTôi có thể giúp bạn kiểm tra ngày phép, báo lỗi IT, hoặc tra cứu quy định công ty.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Tự động cuộn xuống tin nhắn mới nhất
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    
    // Thêm tin nhắn của User vào màn hình
    const newUserMsg: Message = { id: Date.now().toString(), sender: 'user', text: userMessage };
    setMessages(prev => [...prev, newUserMsg]);
    setIsLoading(true);


    try {
      // http://localhost:3000/ai/connect
      // Gọi API sang NestJS Gateway

      const response = await fetch('http://localhost:5000/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userMessage, 
          thread_id: 'web-user-session-3' // Để AI nhớ đoạn chat
        })
      });

      const data = await response.json();
      // Thêm phản hồi của AI vào màn hình
      const aiMessage: Message = { id: (Date.now() + 1).toString(), sender: 'ai', text: data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMsg: Message = { id: Date.now().toString(), sender: 'ai', text: 'Xin lỗi, hệ thống đang mất kết nối tới API Gateway (NestJS)!' };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 font-sans">
      
      {/* HEADER */}
      <header className="bg-white shadow-sm p-4 flex items-center justify-between z-10 border-b">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-md">
            AI
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800 tracking-tight">Enterprise Assistant</h1>
            <p className="text-xs text-green-500 flex items-center gap-1.5 font-medium">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              Trực tuyến
            </p>
          </div>
        </div>
      </header>

      {/* CHAT WINDOW */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`p-4 rounded-2xl max-w-[85%] md:max-w-[70%] shadow-sm ${
              msg.sender === 'user' 
                ? 'bg-blue-600 text-white rounded-tr-none' 
                : 'bg-white border border-gray-100 text-gray-800 rounded-tl-none'
            }`}>
              <p className="whitespace-pre-wrap leading-relaxed text-sm md:text-base">{msg.text}</p>
            </div>
          </div>
        ))}

        {/* TYPING INDICATOR */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-100 p-5 rounded-2xl rounded-tl-none shadow-sm flex gap-1.5 items-center">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* INPUT BOX */}
      <footer className="bg-white border-t border-gray-200 p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto flex gap-3">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Nhập yêu cầu (VD: Báo lỗi máy in, Tra cứu nội quy)..." 
            className="flex-1 px-5 py-3.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-gray-700 placeholder-gray-400"
            disabled={isLoading}
          />
          <button 
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white px-8 py-3.5 rounded-xl font-medium transition-colors shadow-sm"
          >
            Gửi
          </button>
        </form>
      </footer>
      
    </div>
  );
}
