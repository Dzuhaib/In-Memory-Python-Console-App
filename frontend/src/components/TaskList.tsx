'use client';

import { Task, UpdateTaskRequest } from '@/types/task';
import { TaskItem } from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  onToggleComplete: (id: number) => Promise<void>;
  onUpdate: (id: number, request: UpdateTaskRequest) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onAddTag: (id: number, tag: string) => Promise<void>;
  onRemoveTag: (id: number, tag: string) => Promise<void>;
}

export function TaskList({
  tasks,
  loading,
  error,
  onToggleComplete,
  onUpdate,
  onDelete,
  onAddTag,
  onRemoveTag,
}: TaskListProps) {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="spinner" />
        <span className="ml-3 text-gray-500">Loading tasks...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
        <p className="text-red-600">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-2 text-sm text-red-500 underline hover:text-red-700"
        >
          Try again
        </button>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">No tasks found</p>
        <p className="text-gray-400 mt-2">
          Add a new task using the form above, or adjust your filters.
        </p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-700 mb-4">
        Tasks ({tasks.length})
      </h2>
      <div className="space-y-2">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggleComplete={onToggleComplete}
            onUpdate={onUpdate}
            onDelete={onDelete}
            onAddTag={onAddTag}
            onRemoveTag={onRemoveTag}
          />
        ))}
      </div>
    </div>
  );
}
