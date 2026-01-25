'use client';

import { useTasks } from '@/hooks/useTasks';
import { TaskForm } from '@/components/TaskForm';
import { TaskList } from '@/components/TaskList';
import { CreateTaskRequest } from '@/types/task';

export default function Home() {
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
  } = useTasks();

  // Wrappers to match component's expected signatures (Promise<void>)
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

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-3xl mx-auto px-4">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
          <p className="text-gray-600 mt-2">Manage your tasks efficiently</p>
        </header>

        {/* Task Creation Form - never disabled, users can always add tasks */}
        <TaskForm onSubmit={handleCreateTask} />

        {/* Search Bar */}
        <div className="bg-white p-4 rounded-lg shadow mb-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Search Input */}
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search
              </label>
              <input
                type="text"
                id="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search tasks..."
                className="input"
              />
            </div>

            {/* Status Filter */}
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                id="status"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="select"
              >
                <option value="">All</option>
                <option value="complete">Complete</option>
                <option value="incomplete">Incomplete</option>
              </select>
            </div>

            {/* Priority Filter */}
            <div>
              <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                id="priority"
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="select"
              >
                <option value="">All</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>

            {/* Sort Select */}
            <div>
              <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                id="sort"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="select"
              >
                <option value="id">Created (newest)</option>
                <option value="priority">Priority</option>
                <option value="alpha">Alphabetical</option>
              </select>
            </div>
          </div>

          {/* Tag Filter */}
          <div className="mt-4">
            <label htmlFor="tag" className="block text-sm font-medium text-gray-700 mb-1">
              Filter by Tag
            </label>
            <input
              type="text"
              id="tag"
              value={tagFilter}
              onChange={(e) => setTagFilter(e.target.value)}
              placeholder="Enter tag to filter..."
              className="input"
            />
          </div>

          {/* Clear Filters Button */}
          {(searchTerm || statusFilter || priorityFilter || tagFilter || sortBy !== 'id') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('');
                setPriorityFilter('');
                setTagFilter('');
                setSortBy('id');
              }}
              className="mt-4 text-sm text-blue-600 hover:text-blue-800 underline"
            >
              Clear all filters
            </button>
          )}
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
    </main>
  );
}
