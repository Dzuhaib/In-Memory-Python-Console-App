'use client';

import { useState } from 'react';
import { Task, Priority, UpdateTaskRequest } from '@/types/task';

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: number) => Promise<void>;
  onUpdate: (id: number, request: UpdateTaskRequest) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onAddTag: (id: number, tag: string) => Promise<void>;
  onRemoveTag: (id: number, tag: string) => Promise<void>;
}

export function TaskItem({
  task,
  onToggleComplete,
  onUpdate,
  onDelete,
  onAddTag,
  onRemoveTag,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editPriority, setEditPriority] = useState<Priority>(task.priority);
  const [newTag, setNewTag] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggleComplete = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await onToggleComplete(task.id);
    } catch {
      setError('Failed to toggle completion');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    const trimmedTitle = editTitle.trim();
    if (!trimmedTitle) {
      setError('Title cannot be empty');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await onUpdate(task.id, {
        title: trimmedTitle !== task.title ? trimmedTitle : undefined,
        priority: editPriority !== task.priority ? editPriority : undefined,
      });
      setIsEditing(false);
    } catch {
      setError('Failed to update task');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditPriority(task.priority);
    setIsEditing(false);
    setError(null);
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await onDelete(task.id);
    } catch {
      setError('Failed to delete task');
      setIsLoading(false);
    }
  };

  const handleAddTag = async () => {
    const tag = newTag.trim();
    if (!tag) return;

    setIsLoading(true);
    setError(null);
    try {
      await onAddTag(task.id, tag);
      setNewTag('');
    } catch {
      setError('Failed to add tag');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRemoveTag = async (tag: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await onRemoveTag(task.id, tag);
    } catch {
      setError('Failed to remove tag');
    } finally {
      setIsLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="card-premium p-5">
        <div className="space-y-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="input"
            placeholder="Task title"
            maxLength={500}
          />
          <select
            value={editPriority}
            onChange={(e) => setEditPriority(e.target.value as Priority)}
            className="select"
          >
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          {error && <p className="error-message">{error}</p>}
          <div className="flex gap-2">
            <button onClick={handleSaveEdit} className="btn btn-primary" disabled={isLoading}>
              Save Changes
            </button>
            <button onClick={handleCancelEdit} className="btn btn-secondary" disabled={isLoading}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card-premium p-5 group">
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <div className="pt-0.5">
          <button
            onClick={handleToggleComplete}
            disabled={isLoading}
            className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all duration-200 ${
              task.completed
                ? 'bg-indigo-500 border-indigo-500'
                : 'border-gray-300 hover:border-indigo-400'
            }`}
          >
            {task.completed && (
              <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
              </svg>
            )}
          </button>
        </div>

        <div className="flex-1 min-w-0">
          {/* Title */}
          <p className={`text-sm font-medium ${task.completed ? 'task-completed' : 'text-gray-900'}`}>
            {task.title}
          </p>

          {/* Due date and recurrence */}
          {(task.due_at || task.recurrence_rule) && (
            <div className="flex flex-wrap items-center gap-2 mt-1.5">
              {task.due_at && (
                <span className={`inline-flex items-center gap-1 text-xs ${task.is_overdue ? 'text-red-600 font-semibold' : 'text-gray-400'}`}>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                  {task.is_overdue && '! '}
                  {new Date(task.due_at).toLocaleString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              )}
              {task.recurrence_rule && (
                <span className="inline-flex items-center gap-1 text-xs text-indigo-600" title={`Recurs ${task.recurrence_rule}${task.recurrence_interval ? ` (every ${task.recurrence_interval} days)` : ''}`}>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182" />
                  </svg>
                  {task.recurrence_rule === 'every_N_days' ? `every ${task.recurrence_interval} days` : task.recurrence_rule}
                </span>
              )}
            </div>
          )}

          {/* Priority and tags */}
          <div className="flex flex-wrap items-center gap-2 mt-2">
            <span className={`px-2.5 py-1 rounded-full text-xs font-semibold priority-${task.priority}`}>
              {task.priority}
            </span>
            {task.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
                <button
                  onClick={() => handleRemoveTag(tag)}
                  className="ml-0.5 text-indigo-500 hover:text-indigo-800 transition-colors"
                  disabled={isLoading}
                >
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                  </svg>
                </button>
              </span>
            ))}
          </div>

          {/* Add tag */}
          <div className="flex gap-2 mt-2.5">
            <input
              type="text"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              placeholder="Add tag..."
              className="input text-xs py-2"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddTag();
                }
              }}
              disabled={isLoading}
            />
            <button
              onClick={handleAddTag}
              className="btn btn-secondary text-xs py-2 px-3"
              disabled={isLoading || !newTag.trim()}
            >
              Add
            </button>
          </div>

          {error && <p className="error-message mt-2">{error}</p>}
        </div>

        {/* Actions */}
        <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all duration-200"
            disabled={isLoading}
            title="Edit"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
            </svg>
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
            disabled={isLoading}
            title="Delete"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
