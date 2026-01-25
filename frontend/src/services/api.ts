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

// Log API URL on load (helps debug)
if (typeof window !== 'undefined') {
  console.log('API URL:', API_URL);
}

/**
 * Generic fetch wrapper with error handling and timeout.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
  timeoutMs: number = 15000
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  // Create abort controller for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  } catch (err) {
    clearTimeout(timeoutId);

    if (err instanceof Error) {
      if (err.name === 'AbortError') {
        throw new Error('Request timed out. Please check if the backend is running.');
      }
      // Network errors
      if (err.message === 'Failed to fetch') {
        throw new Error('Cannot connect to API. Check NEXT_PUBLIC_API_URL and CORS settings.');
      }
      throw err;
    }
    throw new Error('An unexpected error occurred');
  }
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
