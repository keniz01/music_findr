import React from "react";

interface ChatMessage {
  id: string;
  query: string;
  response: string;
  timestamp: Date;
}

interface ChatHistoryProps {
  messages: ChatMessage[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  if (messages.length === 0) return null;

  return (
    <div className="space-y-4 p-4">
      {messages.map((message) => (
        <div key={message.id} className="space-y-4">
          {/* User Question - Right aligned */}
          <div className="flex justify-end">
            <div className="max-w-[85%] sm:max-w-[80%] bg-blue-500 text-white rounded-lg px-3 py-2 shadow-sm">
              <p className="text-sm break-words">{message.query}</p>
            </div>
          </div>

          {/* AI Response - Left aligned */}
          <div className="flex justify-start">
            <div className="max-w-[85%] sm:max-w-[80%] bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg px-3 py-2 shadow-sm">
              <p className="text-sm whitespace-pre-wrap break-words text-left">
                {message.response}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatHistory;
