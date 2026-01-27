/**
 * TypeScript types for the AI Chat feature.
 */

export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: Date;
  toolInvocations?: ToolInvocation[];
}

export interface ToolInvocation {
  toolCallId: string;
  toolName: string;
  args: Record<string, unknown>;
  result?: unknown;
  state: 'pending' | 'result' | 'error';
}

export type ToolName =
  | 'createTask'
  | 'getTasks'
  | 'getTask'
  | 'updateTask'
  | 'deleteTask'
  | 'toggleComplete'
  | 'addTag'
  | 'removeTag';

export interface CreateTaskArgs {
  title: string;
  priority?: 'high' | 'medium' | 'low';
  tags?: string[];
}

export interface GetTasksArgs {
  search?: string;
  status?: 'complete' | 'incomplete';
  priority?: 'high' | 'medium' | 'low';
  tag?: string;
  sort?: 'priority' | 'alpha' | 'id';
}

export interface GetTaskArgs {
  taskId: number;
}

export interface UpdateTaskArgs {
  taskId: number;
  title?: string;
  priority?: 'high' | 'medium' | 'low';
}

export interface DeleteTaskArgs {
  taskId: number;
}

export interface ToggleCompleteArgs {
  taskId: number;
}

export interface AddTagArgs {
  taskId: number;
  tag: string;
}

export interface RemoveTagArgs {
  taskId: number;
  tag: string;
}

export type ToolArgs =
  | CreateTaskArgs
  | GetTasksArgs
  | GetTaskArgs
  | UpdateTaskArgs
  | DeleteTaskArgs
  | ToggleCompleteArgs
  | AddTagArgs
  | RemoveTagArgs;

export interface ChatRequest {
  messages: {
    role: 'user' | 'assistant';
    content: string;
  }[];
}

export interface ChatError {
  code: 'invalid_request' | 'unauthorized' | 'rate_limited' | 'internal_error';
  message: string;
}
