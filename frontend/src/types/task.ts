/**
 * TypeScript types for the Todo application.
 */

export type Priority = 'high' | 'medium' | 'low';

export interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  priority?: Priority;
  tags?: string[];
}

export interface UpdateTaskRequest {
  title?: string;
  priority?: Priority;
}

export interface AddTagRequest {
  tag: string;
}

export interface TaskQueryParams {
  search?: string;
  status?: 'complete' | 'incomplete';
  priority?: Priority;
  tag?: string;
  sort?: 'priority' | 'alpha' | 'id';
}

export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface ErrorResponse {
  detail: string;
}
