'use client';

import { useTasks } from '@/hooks/useTasks';
import { TaskForm } from '@/components/TaskForm';
import { TaskList } from '@/components/TaskList';
import { CreateTaskRequest } from '@/types/task';

export default function TasksPage() {
  const {
    tasks,
    loading,
    error,
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
    dueBefore,
    setDueBefore,
    dueAfter,
    setDueAfter,
    overdueOnly,
    setOverdueOnly,
  } = useTasks();

  const handleCreateTask = async (request: CreateTaskRequest): Promise<void> => {
    await createTask(request);
  };

  const handleToggleComplete = async (id: number): Promise<void> => {
    await toggleComplete(id);
  };

  const handleUpdate = async (id: number, request: import('@/types/task').UpdateTaskRequest): Promise<void> => {
    await updateTask(id, request);
  };

  const handleDelete = async (id: number): Promise<void> => {
    await deleteTask(id);
  };

  const handleAddTag = async (id: number, tag: string): Promise<void> => {
    await addTag(id, tag);
  };

  const handleRemoveTag = async (id: number, tag: string): Promise<void> => {
    await removeTag(id, tag);
  };

  const hasFilters = searchTerm || statusFilter || priorityFilter || tagFilter || sortBy !== 'id' || dueBefore || dueAfter || overdueOnly;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Add Task */}
      <TaskForm onSubmit={handleCreateTask} />

      {/* Filters */}
      <div className="card-premium p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-700">Filters & Sort</h3>
          {hasFilters && (
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('');
                setPriorityFilter('');
                setTagFilter('');
                setSortBy('id');
                setDueBefore('');
                setDueAfter('');
                setOverdueOnly(false);
              }}
              className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
            >
              Clear all
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          <div>
            <label htmlFor="search" className="block text-xs font-medium text-gray-500 mb-1">Search</label>
            <div className="relative">
              <div className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
              </div>
              <input
                type="text"
                id="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search tasks..."
                className="input pl-10"
              />
            </div>
          </div>
          <div>
            <label htmlFor="status" className="block text-xs font-medium text-gray-500 mb-1">Status</label>
            <select id="status" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="select">
              <option value="">All</option>
              <option value="complete">Complete</option>
              <option value="incomplete">Incomplete</option>
            </select>
          </div>
          <div>
            <label htmlFor="priority" className="block text-xs font-medium text-gray-500 mb-1">Priority</label>
            <select id="priority" value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)} className="select">
              <option value="">All</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
          <div>
            <label htmlFor="sort" className="block text-xs font-medium text-gray-500 mb-1">Sort By</label>
            <select id="sort" value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="select">
              <option value="id">Created (newest)</option>
              <option value="priority">Priority</option>
              <option value="alpha">Alphabetical</option>
              <option value="due_date">Due Date</option>
              <option value="created_at">Created At</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mt-3">
          <div>
            <label htmlFor="tag" className="block text-xs font-medium text-gray-500 mb-1">Tag</label>
            <input
              type="text"
              id="tag"
              value={tagFilter}
              onChange={(e) => setTagFilter(e.target.value)}
              placeholder="Filter by tag..."
              className="input"
            />
          </div>
          <div>
            <label htmlFor="due-after" className="block text-xs font-medium text-gray-500 mb-1">Due After</label>
            <input type="datetime-local" id="due-after" value={dueAfter} onChange={(e) => setDueAfter(e.target.value)} className="input" />
          </div>
          <div>
            <label htmlFor="due-before" className="block text-xs font-medium text-gray-500 mb-1">Due Before</label>
            <input type="datetime-local" id="due-before" value={dueBefore} onChange={(e) => setDueBefore(e.target.value)} className="input" />
          </div>
          <div className="flex items-end">
            <label className="flex items-center gap-2.5 pb-3 cursor-pointer">
              <input
                type="checkbox"
                checked={overdueOnly}
                onChange={(e) => setOverdueOnly(e.target.checked)}
                className="h-4 w-4 rounded-md border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span className="text-sm text-gray-600 font-medium">Overdue only</span>
            </label>
          </div>
        </div>
      </div>

      {/* Task List */}
      <TaskList
        tasks={tasks}
        loading={loading}
        error={error}
        onToggleComplete={handleToggleComplete}
        onUpdate={handleUpdate}
        onDelete={handleDelete}
        onAddTag={handleAddTag}
        onRemoveTag={handleRemoveTag}
      />
    </div>
  );
}
