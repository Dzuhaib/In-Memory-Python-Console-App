'use client';

import { useState, useCallback, useEffect } from 'react';
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskQueryParams,
  Priority,
} from '@/types/task';
import * as api from '@/services/api';

interface UseTasksState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

interface UseTasksReturn extends UseTasksState {
  fetchTasks: (params?: TaskQueryParams) => Promise<void>;
  createTask: (request: CreateTaskRequest) => Promise<Task | null>;
  updateTask: (id: number, request: UpdateTaskRequest) => Promise<Task | null>;
  deleteTask: (id: number) => Promise<boolean>;
  toggleComplete: (id: number) => Promise<Task | null>;
  addTag: (id: number, tag: string) => Promise<Task | null>;
  removeTag: (id: number, tag: string) => Promise<Task | null>;
  // Query state
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  statusFilter: string;
  setStatusFilter: (status: string) => void;
  priorityFilter: string;
  setPriorityFilter: (priority: string) => void;
  tagFilter: string;
  setTagFilter: (tag: string) => void;
  sortBy: string;
  setSortBy: (sort: string) => void;
}

export function useTasks(): UseTasksReturn {
  const [state, setState] = useState<UseTasksState>({
    tasks: [],
    loading: true,
    error: null,
  });

  // Query state
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [tagFilter, setTagFilter] = useState('');
  const [sortBy, setSortBy] = useState('id');

  const fetchTasks = useCallback(async (params?: TaskQueryParams) => {
    setState((prev) => ({ ...prev, loading: true, error: null }));
    try {
      const tasks = await api.getTasks(params);
      setState({ tasks, loading: false, error: null });
    } catch (err) {
      setState((prev) => ({
        ...prev,
        loading: false,
        error: err instanceof Error ? err.message : 'Failed to fetch tasks',
      }));
    }
  }, []);

  // Fetch tasks when query params change
  useEffect(() => {
    const params: TaskQueryParams = {};
    if (searchTerm) params.search = searchTerm;
    if (statusFilter) params.status = statusFilter as 'complete' | 'incomplete';
    if (priorityFilter) params.priority = priorityFilter as Priority;
    if (tagFilter) params.tag = tagFilter;
    if (sortBy) params.sort = sortBy as 'priority' | 'alpha' | 'id';

    fetchTasks(params);
  }, [searchTerm, statusFilter, priorityFilter, tagFilter, sortBy, fetchTasks]);

  // Listen for tasks-updated event from chat widget
  useEffect(() => {
    const handleTasksUpdated = () => {
      const params: TaskQueryParams = {};
      if (searchTerm) params.search = searchTerm;
      if (statusFilter) params.status = statusFilter as 'complete' | 'incomplete';
      if (priorityFilter) params.priority = priorityFilter as Priority;
      if (tagFilter) params.tag = tagFilter;
      if (sortBy) params.sort = sortBy as 'priority' | 'alpha' | 'id';
      fetchTasks(params);
    };

    window.addEventListener('tasks-updated', handleTasksUpdated);
    return () => window.removeEventListener('tasks-updated', handleTasksUpdated);
  }, [searchTerm, statusFilter, priorityFilter, tagFilter, sortBy, fetchTasks]);

  const createTask = useCallback(async (request: CreateTaskRequest): Promise<Task | null> => {
    try {
      const task = await api.createTask(request);
      setState((prev) => ({
        ...prev,
        tasks: [...prev.tasks, task],
      }));
      return task;
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: err instanceof Error ? err.message : 'Failed to create task',
      }));
      return null;
    }
  }, []);

  const updateTask = useCallback(
    async (id: number, request: UpdateTaskRequest): Promise<Task | null> => {
      try {
        const task = await api.updateTask(id, request);
        setState((prev) => ({
          ...prev,
          tasks: prev.tasks.map((t) => (t.id === id ? task : t)),
        }));
        return task;
      } catch (err) {
        setState((prev) => ({
          ...prev,
          error: err instanceof Error ? err.message : 'Failed to update task',
        }));
        return null;
      }
    },
    []
  );

  const deleteTask = useCallback(async (id: number): Promise<boolean> => {
    try {
      await api.deleteTask(id);
      setState((prev) => ({
        ...prev,
        tasks: prev.tasks.filter((t) => t.id !== id),
      }));
      return true;
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: err instanceof Error ? err.message : 'Failed to delete task',
      }));
      return false;
    }
  }, []);

  const toggleComplete = useCallback(async (id: number): Promise<Task | null> => {
    try {
      const task = await api.toggleComplete(id);
      setState((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) => (t.id === id ? task : t)),
      }));
      return task;
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: err instanceof Error ? err.message : 'Failed to toggle completion',
      }));
      return null;
    }
  }, []);

  const addTag = useCallback(async (id: number, tag: string): Promise<Task | null> => {
    try {
      const task = await api.addTag(id, tag);
      setState((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) => (t.id === id ? task : t)),
      }));
      return task;
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: err instanceof Error ? err.message : 'Failed to add tag',
      }));
      return null;
    }
  }, []);

  const removeTag = useCallback(async (id: number, tag: string): Promise<Task | null> => {
    try {
      const task = await api.removeTag(id, tag);
      setState((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) => (t.id === id ? task : t)),
      }));
      return task;
    } catch (err) {
      setState((prev) => ({
        ...prev,
        error: err instanceof Error ? err.message : 'Failed to remove tag',
      }));
      return null;
    }
  }, []);

  return {
    ...state,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
    addTag,
    removeTag,
    searchTerm,
    setSearchTerm,
    statusFilter,
    setStatusFilter,
    priorityFilter,
    setPriorityFilter,
    tagFilter,
    setTagFilter,
    sortBy,
    setSortBy,
  };
}
