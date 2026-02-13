'use client';

import Link from 'next/link';
import { useTasks } from '@/hooks/useTasks';
import { TaskForm } from '@/components/TaskForm';
import { TaskItem } from '@/components/TaskItem';
import { CreateTaskRequest } from '@/types/task';

export default function DashboardPage() {
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
  } = useTasks();

  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((t) => t.completed).length;
  const pendingTasks = totalTasks - completedTasks;
  const overdueTasks = tasks.filter((t) => t.is_overdue).length;
  const highPriority = tasks.filter((t) => t.priority === 'high' && !t.completed).length;
  const recurringTasks = tasks.filter((t) => t.recurrence_rule).length;

  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
  const recentTasks = [...tasks].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()).slice(0, 5);
  const upcomingDue = tasks
    .filter((t) => t.due_at && !t.completed)
    .sort((a, b) => new Date(a.due_at!).getTime() - new Date(b.due_at!).getTime())
    .slice(0, 5);

  const handleCreateTask = async (request: CreateTaskRequest) => {
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

  const stats = [
    {
      label: 'Total Tasks',
      value: totalTasks,
      gradient: 'from-blue-500 to-indigo-600',
      bg: 'bg-blue-50',
      iconBg: 'bg-blue-500/10',
      icon: (
        <svg className="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 0 1 0 3.75H5.625a1.875 1.875 0 0 1 0-3.75Z" />
        </svg>
      ),
    },
    {
      label: 'Completed',
      value: completedTasks,
      sub: `${completionRate}%`,
      gradient: 'from-emerald-500 to-teal-600',
      bg: 'bg-emerald-50',
      iconBg: 'bg-emerald-500/10',
      icon: (
        <svg className="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
        </svg>
      ),
    },
    {
      label: 'Pending',
      value: pendingTasks,
      gradient: 'from-amber-500 to-orange-600',
      bg: 'bg-amber-50',
      iconBg: 'bg-amber-500/10',
      icon: (
        <svg className="w-5 h-5 text-amber-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
        </svg>
      ),
    },
    {
      label: 'Overdue',
      value: overdueTasks,
      gradient: 'from-red-500 to-rose-600',
      bg: 'bg-red-50',
      iconBg: 'bg-red-500/10',
      icon: (
        <svg className="w-5 h-5 text-red-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
        </svg>
      ),
    },
    {
      label: 'High Priority',
      value: highPriority,
      gradient: 'from-orange-500 to-red-600',
      bg: 'bg-orange-50',
      iconBg: 'bg-orange-500/10',
      icon: (
        <svg className="w-5 h-5 text-orange-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15.362 5.214A8.252 8.252 0 0 1 12 21 8.25 8.25 0 0 1 6.038 7.047 8.287 8.287 0 0 0 9 9.601a8.983 8.983 0 0 1 3.361-6.867 8.21 8.21 0 0 0 3 2.48Z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18a3.75 3.75 0 0 0 .495-7.468 5.99 5.99 0 0 0-1.925 3.547 5.975 5.975 0 0 1-2.133-1.001A3.75 3.75 0 0 0 12 18Z" />
        </svg>
      ),
    },
    {
      label: 'Recurring',
      value: recurringTasks,
      gradient: 'from-violet-500 to-purple-600',
      bg: 'bg-violet-50',
      iconBg: 'bg-violet-500/10',
      icon: (
        <svg className="w-5 h-5 text-violet-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182" />
        </svg>
      ),
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="spinner mx-auto mb-4" style={{ width: 40, height: 40 }} />
          <p className="text-gray-400 text-sm font-medium">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="card-premium p-4 group"
          >
            <div className="flex items-center justify-between mb-3">
              <div className={`w-10 h-10 rounded-xl ${stat.iconBg} flex items-center justify-center`}>
                {stat.icon}
              </div>
              {stat.sub && (
                <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
                  {stat.sub}
                </span>
              )}
            </div>
            <p className={`text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r ${stat.gradient}`}>
              {stat.value}
            </p>
            <p className="text-xs text-gray-400 mt-1 font-medium">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Progress Bar */}
      <div className="card-premium p-6">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-gray-700">Overall Progress</h2>
          <span className="text-sm font-bold text-gradient">{completionRate}%</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-indigo-500 via-violet-500 to-purple-500 h-3 rounded-full transition-all duration-700 ease-out"
            style={{ width: `${completionRate}%` }}
          />
        </div>
        <p className="text-xs text-gray-400 mt-2.5">
          {completedTasks} of {totalTasks} tasks completed
        </p>
      </div>

      {/* Quick Add + Upcoming Due */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-sm font-semibold text-gray-700 mb-3">Quick Add</h2>
          <TaskForm onSubmit={handleCreateTask} />
        </div>

        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-gray-700">Upcoming Due</h2>
            <Link href="/app/tasks" className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors">
              View all
            </Link>
          </div>
          <div className="card-premium p-5">
            {upcomingDue.length === 0 ? (
              <div className="text-center py-8">
                <svg className="w-10 h-10 text-gray-200 mx-auto mb-3" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
                </svg>
                <p className="text-gray-400 text-sm">No upcoming deadlines</p>
              </div>
            ) : (
              <div className="space-y-3">
                {upcomingDue.map((task) => (
                  <div key={task.id} className="flex items-center gap-3 py-2.5 border-b border-gray-50 last:border-0">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleComplete(task.id)}
                      className="h-4 w-4 rounded-md border-gray-300 text-indigo-600 focus:ring-indigo-500"
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900 font-medium truncate">{task.title}</p>
                      <p className={`text-xs mt-0.5 ${task.is_overdue ? 'text-red-500 font-semibold' : 'text-gray-400'}`}>
                        {task.is_overdue && '! '}
                        {task.due_at && new Date(task.due_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold priority-${task.priority}`}>
                      {task.priority}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Tasks */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-gray-700">Recent Tasks</h2>
          <Link href="/app/tasks" className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors">
            View all
          </Link>
        </div>
        {error && (
          <div className="bg-red-50 border border-red-100 rounded-xl p-4 mb-4 flex items-start gap-3">
            <svg className="w-5 h-5 text-red-500 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
            </svg>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}
        <div className="space-y-2">
          {recentTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
              onAddTag={handleAddTag}
              onRemoveTag={handleRemoveTag}
            />
          ))}
          {recentTasks.length === 0 && (
            <div className="text-center py-16 card-premium">
              <svg className="w-12 h-12 text-gray-200 mx-auto mb-4" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
              </svg>
              <p className="text-gray-400 text-base font-medium mb-1">No tasks yet</p>
              <p className="text-gray-300 text-sm">Create your first task using the form above</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
