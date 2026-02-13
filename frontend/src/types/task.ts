/**
 * TypeScript types for the Todo application.
 * Task T012: Update frontend TypeScript Task interface with Phase 5 fields
 */

export type Priority = 'high' | 'medium' | 'low';
export type RecurrenceRule = 'daily' | 'weekly' | 'monthly' | 'every_N_days';

export interface Task {
  id: number;
  title: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  created_at: string;
  updated_at: string;
  // Phase 5 extensions (T012)
  due_at: string | null;
  remind_at: string | null;
  recurrence_rule: RecurrenceRule | null;
  recurrence_interval: number | null;
  is_overdue: boolean;
}

export interface CreateTaskRequest {
  title: string;
  priority?: Priority;
  tags?: string[];
  // Phase 5 extensions (T012)
  due_at?: string | null;
  remind_at?: string | null;
  recurrence_rule?: RecurrenceRule | null;
  recurrence_interval?: number | null;
}

export interface UpdateTaskRequest {
  title?: string;
  priority?: Priority;
  // Phase 5 extensions (T012)
  due_at?: string | null;
  remind_at?: string | null;
  recurrence_rule?: RecurrenceRule | null;
  recurrence_interval?: number | null;
}

export interface AddTagRequest {
  tag: string;
}

export interface TaskQueryParams {
  search?: string;
  status?: 'complete' | 'incomplete';
  priority?: Priority;
  tag?: string;
  sort?: 'priority' | 'alpha' | 'id' | 'due_date' | 'created_at';
  // Phase 5 extensions for US3 (T038)
  due_before?: string;
  due_after?: string;
  overdue?: boolean;
  sort_dir?: 'asc' | 'desc';
}

export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface ErrorResponse {
  detail: string;
}
