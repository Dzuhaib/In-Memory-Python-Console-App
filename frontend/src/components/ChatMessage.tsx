'use client';

/**
 * ChatMessage component - Renders a single chat message.
 */

export interface MessagePart {
  type: string;
  text?: string;
  toolCallId?: string;
  toolName?: string;
  args?: Record<string, unknown>;
  result?: string;
}

export interface ChatMessageData {
  id: string;
  role: 'user' | 'assistant' | 'system';
  parts?: MessagePart[];
  content?: string;
}

interface ChatMessageProps {
  message: ChatMessageData;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  // Extract text content from parts or use content directly
  const textContent = message.parts
    ? message.parts
        .filter((part) => part.type === 'text')
        .map((part) => part.text)
        .join('')
    : message.content || '';

  // Extract tool calls from parts
  const toolCalls = message.parts?.filter(
    (part) => part.type === 'tool-invocation' || part.type === 'tool-result'
  );

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-900'
        }`}
      >
        {/* Role indicator */}
        <div className={`text-xs mb-1 ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
          {isUser ? 'You' : 'Assistant'}
        </div>

        {/* Message content */}
        <div className="whitespace-pre-wrap text-sm">
          {textContent}
        </div>

        {/* Tool invocations display */}
        {toolCalls && toolCalls.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-200">
            {toolCalls.map((tc, index) => (
              <div key={tc.toolCallId || index} className="text-xs text-gray-500">
                <span className="font-medium">Tool: </span>
                {tc.toolName}
                {tc.result && (
                  <span className="ml-1 text-green-600">✓</span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;
