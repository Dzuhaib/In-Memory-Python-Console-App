'use client';

import { useState, FormEvent } from 'react';
import { CreateTaskRequest, Priority } from '@/types/task';

interface TaskFormProps {
  onSubmit: (request: CreateTaskRequest) => Promise<void>;
  disabled?: boolean;
}

export function TaskForm({ onSubmit, disabled = false }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [tagsInput, setTagsInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setError('Title is required');
      return;
    }

    setIsSubmitting(true);
    try {
      const tags = tagsInput
        .split(',')
        .map((t) => t.trim())
        .filter((t) => t.length > 0);

      await onSubmit({
        title: trimmedTitle,
        priority,
        tags: tags.length > 0 ? tags : undefined,
      });

      // Reset form on success
      setTitle('');
      setPriority('medium');
      setTagsInput('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow mb-6">
      <h2 className="text-lg font-semibold mb-4">Add New Task</h2>

      <div className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter task title..."
            className="input"
            disabled={disabled || isSubmitting}
            maxLength={500}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              id="priority"
              value={priority}
              onChange={(e) => setPriority(e.target.value as Priority)}
              className="select"
              disabled={disabled || isSubmitting}
            >
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div>
            <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-1">
              Tags (comma-separated)
            </label>
            <input
              type="text"
              id="tags"
              value={tagsInput}
              onChange={(e) => setTagsInput(e.target.value)}
              placeholder="work, urgent, personal..."
              className="input"
              disabled={disabled || isSubmitting}
            />
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}

        <button
          type="submit"
          className="btn btn-primary w-full"
          disabled={disabled || isSubmitting}
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center">
              <span className="spinner mr-2" />
              Adding...
            </span>
          ) : (
            'Add Task'
          )}
        </button>
      </div>
    </form>
  );
}
