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
    } catch (err) {
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
    } catch (err) {
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
    } catch (err) {
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
    } catch (err) {
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
    } catch (err) {
      setError('Failed to remove tag');
    } finally {
      setIsLoading(false);
    }
  };

  const priorityClass = `priority-${task.priority}`;

  if (isEditing) {
    return (
      <div className="bg-white p-4 rounded-lg shadow mb-2">
        <div className="space-y-3">
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
            <button
              onClick={handleSaveEdit}
              className="btn btn-primary"
              disabled={isLoading}
            >
              Save
            </button>
            <button
              onClick={handleCancelEdit}
              className="btn btn-secondary"
              disabled={isLoading}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-2">
      <div className="flex items-start gap-3">
        {/* Completion checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          disabled={isLoading}
          className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />

        <div className="flex-1 min-w-0">
          {/* Title */}
          <p className={`text-lg ${task.completed ? 'task-completed' : 'text-gray-900'}`}>
            {task.title}
          </p>

          {/* Priority and tags */}
          <div className="flex flex-wrap items-center gap-2 mt-2">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${priorityClass}`}>
              {task.priority}
            </span>
            {task.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
                <button
                  onClick={() => handleRemoveTag(tag)}
                  className="ml-1 text-blue-600 hover:text-blue-800"
                  disabled={isLoading}
                >
                  ×
                </button>
              </span>
            ))}
          </div>

          {/* Add tag input */}
          <div className="flex gap-2 mt-2">
            <input
              type="text"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              placeholder="Add tag..."
              className="input text-sm py-1"
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
              className="btn btn-secondary text-sm py-1"
              disabled={isLoading || !newTag.trim()}
            >
              Add
            </button>
          </div>

          {error && <p className="error-message mt-2">{error}</p>}
        </div>

        {/* Action buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => setIsEditing(true)}
            className="text-gray-500 hover:text-blue-600"
            disabled={isLoading}
            title="Edit"
          >
            ✏️
          </button>
          <button
            onClick={handleDelete}
            className="text-gray-500 hover:text-red-600"
            disabled={isLoading}
            title="Delete"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  );
}
