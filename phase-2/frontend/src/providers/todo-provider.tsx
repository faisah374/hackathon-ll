'use client';

import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
  useCallback
} from 'react';
import { useAuth } from '@/providers/auth-provider';

/* =======================
   Types
======================= */
interface Todo {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

interface TodoContextType {
  todos: Todo[];
  isLoading: boolean;
  isCreating: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  error: string | null;
  fetchTodos: () => Promise<void>;
  createTodo: (title: string, description?: string) => Promise<Todo>;
  updateTodo: (id: string, updates: Partial<Todo>) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
}

/* =======================
   Context
======================= */
const TodoContext = createContext<TodoContextType | undefined>(undefined);

/* =======================
   Provider
======================= */
export function TodoProvider({ children }: { children: ReactNode }) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { user } = useAuth();

  /* =======================
     Fetch Todos
  ======================= */
  const fetchTodos = useCallback(async () => {
    if (!user) {
      setTodos([]);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      const storedTodos = localStorage.getItem(`todos-${user.id}`);
      setTodos(storedTodos ? JSON.parse(storedTodos) : []);
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError('Failed to fetch todos.');
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  /* =======================
     Fetch on User Change
  ======================= */
  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  /* =======================
     Create Todo
  ======================= */
  const createTodo = async (title: string, description?: string) => {
    if (!user) throw new Error('User not authenticated');
    if (!title.trim()) throw new Error('Title is required');

    try {
      setIsCreating(true);
      setError(null);

      const newTodo: Todo = {
        id: Date.now().toString(),
        userId: user.id,
        title: title.trim(),
        description: description?.trim(),
        completed: false,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      const updatedTodos = [...todos, newTodo];
      setTodos(updatedTodos);
      localStorage.setItem(`todos-${user.id}`, JSON.stringify(updatedTodos));

      return newTodo;
    } catch (err) {
      console.error('Error creating todo:', err);
      setError('Failed to create todo.');
      throw err;
    } finally {
      setIsCreating(false);
    }
  };

  /* =======================
     Update Todo
  ======================= */
  const updateTodo = async (id: string, updates: Partial<Todo>) => {
    if (!user) throw new Error('User not authenticated');

    try {
      setIsUpdating(true);
      setError(null);

      const updatedTodos = todos.map(todo =>
        todo.id === id
          ? { ...todo, ...updates, updatedAt: new Date().toISOString() }
          : todo
      );

      setTodos(updatedTodos);
      localStorage.setItem(`todos-${user.id}`, JSON.stringify(updatedTodos));
    } catch (err) {
      console.error('Error updating todo:', err);
      setError('Failed to update todo.');
      throw err;
    } finally {
      setIsUpdating(false);
    }
  };

  /* =======================
     Delete Todo
  ======================= */
  const deleteTodo = async (id: string) => {
    if (!user) throw new Error('User not authenticated');

    try {
      setIsDeleting(true);
      setError(null);

      const updatedTodos = todos.filter(todo => todo.id !== id);
      setTodos(updatedTodos);
      localStorage.setItem(`todos-${user.id}`, JSON.stringify(updatedTodos));
    } catch (err) {
      console.error('Error deleting todo:', err);
      setError('Failed to delete todo.');
      throw err;
    } finally {
      setIsDeleting(false);
    }
  };

  /* =======================
     Toggle Todo
  ======================= */
  const toggleTodo = async (id: string) => {
    if (!user) throw new Error('User not authenticated');

    try {
      setIsUpdating(true);
      setError(null);

      const updatedTodos = todos.map(todo =>
        todo.id === id
          ? {
              ...todo,
              completed: !todo.completed,
              updatedAt: new Date().toISOString()
            }
          : todo
      );

      setTodos(updatedTodos);
      localStorage.setItem(`todos-${user.id}`, JSON.stringify(updatedTodos));
    } catch (err) {
      console.error('Error toggling todo:', err);
      setError('Failed to update todo.');
      throw err;
    } finally {
      setIsUpdating(false);
    }
  };

  /* =======================
     Context Value
  ======================= */
  const value: TodoContextType = {
    todos,
    isLoading,
    isCreating,
    isUpdating,
    isDeleting,
    error,
    fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    toggleTodo
  };

  return <TodoContext.Provider value={value}>{children}</TodoContext.Provider>;
}

/* =======================
   Hook
======================= */
export function useTodo() {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodo must be used within a TodoProvider');
  }
  return context;
}
