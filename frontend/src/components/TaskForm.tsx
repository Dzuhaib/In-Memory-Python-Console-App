'use client';

import { useState, FormEvent } from 'react';
import { CreateTaskRequest, Priority, RecurrenceRule } from '@/types/task';

interface TaskFormProps {
  onSubmit: (request: CreateTaskRequest) => Promise<void>;
  disabled?: boolean;
}

export function TaskForm({ onSubmit, disabled = false }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState<Priority>('medium');
  const [tagsInput, setTagsInput] = useState('');
  const [dueAt, setDueAt] = useState('');
  const [remindAt, setRemindAt] = useState('');
  const [recurrenceRule, setRecurrenceRule] = useState('');
  const [recurrenceInterval, setRecurrenceInterval] = useState('1');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);

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
        due_at: dueAt || undefined,
        remind_at: remindAt || undefined,
        recurrence_rule: recurrenceRule ? (recurrenceRule as RecurrenceRule) : undefined,
        recurrence_interval: recurrenceRule === 'every_N_days' ? parseInt(recurrenceInterval, 10) : undefined,
      });

      setTitle('');
      setPriority('medium');
      setTagsInput('');
      setDueAt('');
      setRemindAt('');
      setRecurrenceRule('');
      setRecurrenceInterval('1');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card-premium p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-700">Add New Task</h2>
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
        >
          {showAdvanced ? 'Simple' : 'Advanced'}
        </button>
      </div>

      <div className="space-y-4">
        {/* Title */}
        <div>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            className="input"
            disabled={disabled || isSubmitting}
            maxLength={500}
          />
        </div>

        {/* Priority and Tags row */}
        <div className="grid grid-cols-2 gap-3">
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as Priority)}
            className="select"
            disabled={disabled || isSubmitting}
          >
            <option value="high">High Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="low">Low Priority</option>
          </select>

          <input
            type="text"
            id="tags"
            value={tagsInput}
            onChange={(e) => setTagsInput(e.target.value)}
            placeholder="Tags (comma-separated)"
            className="input"
            disabled={disabled || isSubmitting}
          />
        </div>

        {/* Advanced fields */}
        {showAdvanced && (
          <div className="space-y-3 pt-2 border-t border-gray-100 animate-fade-in">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label htmlFor="due-at" className="block text-xs font-medium text-gray-500 mb-1">
                  Due Date
                </label>
                <input
                  type="datetime-local"
                  id="due-at"
                  value={dueAt}
                  onChange={(e) => setDueAt(e.target.value)}
                  className="input"
                  disabled={disabled || isSubmitting}
                />
              </div>
              <div>
                <label htmlFor="remind-at" className="block text-xs font-medium text-gray-500 mb-1">
                  Reminder
                </label>
                <input
                  type="datetime-local"
                  id="remind-at"
                  value={remindAt}
                  onChange={(e) => setRemindAt(e.target.value)}
                  className="input"
                  disabled={disabled || isSubmitting}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label htmlFor="recurrence" className="block text-xs font-medium text-gray-500 mb-1">
                  Recurrence
                </label>
                <select
                  id="recurrence"
                  value={recurrenceRule}
                  onChange={(e) => setRecurrenceRule(e.target.value)}
                  className="select"
                  disabled={disabled || isSubmitting}
                >
                  <option value="">None</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="every_N_days">Custom (every N days)</option>
                </select>
              </div>

              {recurrenceRule === 'every_N_days' && (
                <div>
                  <label htmlFor="recurrence-interval" className="block text-xs font-medium text-gray-500 mb-1">
                    Interval (days)
                  </label>
                  <input
                    type="number"
                    id="recurrence-interval"
                    value={recurrenceInterval}
                    onChange={(e) => setRecurrenceInterval(e.target.value)}
                    min="1"
                    className="input"
                    disabled={disabled || isSubmitting}
                  />
                </div>
              )}
            </div>
          </div>
        )}

        {error && <p className="error-message">{error}</p>}

        <button
          type="submit"
          className="btn btn-primary w-full"
          disabled={disabled || isSubmitting}
        >
          {isSubmitting ? (
            <span className="flex items-center justify-center gap-2">
              <span className="spinner" style={{ width: 16, height: 16 }} />
              Adding...
            </span>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              Add Task
            </>
          )}
        </button>
      </div>
    </form>
  );
}
