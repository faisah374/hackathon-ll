'use client';

import { useEffect } from 'react';
import { useAuth } from '@/providers/auth-provider';
import { useTodo } from '@/providers/todo-provider';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/protected-route';
import TodoList from '@/components/todos/todo-list';
import TodoForm from '@/components/todos/todo-form';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuth();
  const { fetchTodos, todos, isLoading } = useTodo();

  useEffect(() => {
    if (user) {
      fetchTodos();
    }
  }, [user, fetchTodos]);

  const handleLogout = () => {
    logout();
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.name || user?.email}</span>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="mb-8">
            <TodoForm />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Your Todos</h2>
            {isLoading ? (
              <div className="text-center py-8">Loading todos...</div>
            ) : (
              <TodoList todos={todos} />
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}