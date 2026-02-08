'use client';

/**
 * ChatWindow component - Main chat interface that composes ChatMessage and ChatInput.
 */

import { useRef, useEffect } from 'react';
import { ChatMessage, ChatMessageData } from './ChatMessage';
import { ChatInput } from './ChatInput';

interface ChatWindowProps {
  messages: ChatMessageData[];
  onSubmit: (message: string) => void;
  isLoading?: boolean;
}

export function ChatWindow({ messages, onSubmit, isLoading = false }: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex flex-col h-full">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p className="text-lg font-medium mb-2">Welcome to the AI Todo Assistant!</p>
            <p className="text-sm">Try saying things like:</p>
            <ul className="text-sm mt-2 space-y-1">
              <li>&quot;Add a task to buy groceries&quot;</li>
              <li>&quot;Show me my tasks&quot;</li>
              <li>&quot;Mark task 1 as done&quot;</li>
              <li>&quot;Delete task 2&quot;</li>
              <li>&quot;Help&quot;</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <div className="flex items-center space-x-2">
                <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '0ms' }} />
                <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '150ms' }} />
                <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input container */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <ChatInput
          onSubmit={onSubmit}
          isLoading={isLoading}
          placeholder="Type your message... (e.g., 'Add a task to buy milk')"
        />
      </div>
    </div>
  );
}

export default ChatWindow;
