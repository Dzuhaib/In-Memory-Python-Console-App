'use client';

/**
 * Floating Chat Widget - AI-powered todo assistant.
 * Appears as a floating button at bottom-right, expands to chat interface.
 */

import { useState, useCallback, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL?.replace('/api/v1', '') || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const assistantId = (Date.now() + 1).toString();
      let assistantContent = '';

      // Add empty assistant message
      setMessages((prev) => [
        ...prev,
        { id: assistantId, role: 'assistant', content: '' },
      ]);

      // Read streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') continue;

              try {
                const parsed = JSON.parse(data);
                if (parsed.error) {
                  setError(parsed.error);
                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === assistantId
                        ? { ...msg, content: `Error: ${parsed.error}` }
                        : msg
                    )
                  );
                } else if (parsed.content) {
                  assistantContent += parsed.content;
                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === assistantId
                        ? { ...msg, content: assistantContent }
                        : msg
                    )
                  );
                }
              } catch {
                // Ignore parse errors
              }
            }
          }
        }
      }
      // Dispatch event to refresh tasks after chat action completes
      window.dispatchEvent(new CustomEvent('tasks-updated'));
    } catch (err) {
      console.error('Chat error:', err);
      setError(err instanceof Error ? err.message : 'Failed to connect');
    } finally {
      setIsLoading(false);
    }
  }, [input, isLoading]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all duration-200 z-50"
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[500px] bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col z-50 overflow-hidden">
          {/* Header */}
          <div className="bg-blue-600 text-white px-4 py-3 flex items-center justify-between">
            <div>
              <h3 className="font-semibold">AI Todo Assistant</h3>
              <p className="text-xs text-blue-200">Powered by OpenAI</p>
            </div>
            <div className="flex items-center gap-2">
              {messages.length > 0 && (
                <button
                  onClick={clearChat}
                  className="text-xs text-blue-200 hover:text-white"
                  title="Clear chat"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="bg-red-50 border-b border-red-200 px-4 py-2 text-sm text-red-600">
              {error}
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 py-4">
                <p className="text-sm font-medium mb-2">Welcome!</p>
                <p className="text-xs mb-3">Try saying:</p>
                <div className="space-y-1 text-xs">
                  <p className="bg-white rounded px-2 py-1">&quot;Add a task to buy groceries&quot;</p>
                  <p className="bg-white rounded px-2 py-1">&quot;Show me my tasks&quot;</p>
                  <p className="bg-white rounded px-2 py-1">&quot;Mark task 1 as done&quot;</p>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-900 border border-gray-200'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content || '...'}</div>
                  </div>
                </div>
              ))
            )}

            {isLoading && messages[messages.length - 1]?.role === 'user' && (
              <div className="flex justify-start">
                <div className="bg-white rounded-lg px-3 py-2 border border-gray-200">
                  <div className="flex items-center space-x-1">
                    <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '0ms' }} />
                    <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '150ms' }} />
                    <div className="animate-bounce h-2 w-2 bg-gray-400 rounded-full" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-3 bg-white">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
                disabled={isLoading}
                className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100"
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || isLoading}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
