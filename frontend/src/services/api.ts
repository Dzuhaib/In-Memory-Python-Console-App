/**
 * API client service for communicating with the FastAPI backend.
 */

import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  AddTagRequest,
  TaskQueryParams,
  HealthResponse,
} from '@/types/task';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * Generic fetch wrapper with error handling.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

/**
 * Build query string from params object.
 */
function buildQueryString(params: TaskQueryParams): string {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      searchParams.append(key, String(value));
    }
  });
  const queryString = searchParams.toString();
  return queryString ? `?${queryString}` : '';
}

// Task API functions

export async function getTasks(params: TaskQueryParams = {}): Promise<Task[]> {
  const query = buildQueryString(params);
  return fetchApi<Task[]>(`/tasks${query}`);
}

export async function getTask(id: number): Promise<Task> {
  return fetchApi<Task>(`/tasks/${id}`);
}

export async function createTask(request: CreateTaskRequest): Promise<Task> {
  return fetchApi<Task>('/tasks', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function updateTask(id: number, request: UpdateTaskRequest): Promise<Task> {
  return fetchApi<Task>(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(request),
  });
}

export async function deleteTask(id: number): Promise<void> {
  return fetchApi<void>(`/tasks/${id}`, {
    method: 'DELETE',
  });
}

export async function toggleComplete(id: number): Promise<Task> {
  return fetchApi<Task>(`/tasks/${id}/complete`, {
    method: 'PATCH',
  });
}

export async function addTag(id: number, tag: string): Promise<Task> {
  return fetchApi<Task>(`/tasks/${id}/tags`, {
    method: 'POST',
    body: JSON.stringify({ tag } as AddTagRequest),
  });
}

export async function removeTag(id: number, tag: string): Promise<Task> {
  return fetchApi<Task>(`/tasks/${id}/tags/${encodeURIComponent(tag)}`, {
    method: 'DELETE',
  });
}

export async function healthCheck(): Promise<HealthResponse> {
  return fetchApi<HealthResponse>('/health');
}
