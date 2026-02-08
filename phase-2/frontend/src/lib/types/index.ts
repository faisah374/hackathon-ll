// Type definitions for the Todo application

// User types
export interface User {
  id: string;
  email: string;
  name?: string;
}

// Session types
export interface Session {
  user: User;
  token: string;
  expiresAt: Date;
}

// Todo types
export interface Todo {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

// UI State types
export interface UIState {
  currentView: 'dashboard' | 'login' | 'signup' | 'settings';
  showModal: boolean;
  modalType: 'createTodo' | 'editTodo' | 'confirmDelete' | null;
  modalData: any;
  notifications: Notification[];
}

export interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  timestamp: number;
}

// Form State types
export interface TodoFormState {
  title: string;
  description: string;
  errors: {
    title?: string;
    description?: string;
  };
  isSubmitting: boolean;
}

// API Response types
export interface ApiResponse<T> {
  success?: boolean;
  data?: T;
  error?: string;
  errorCode?: string;
}

// Context types
export interface AuthContextType {
  user: User | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => void;
  checkAuthStatus: () => Promise<void>;
}

export interface TodoContextType {
  todos: Todo[];
  isLoading: boolean;
  isCreating: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  error: string | null;
  fetchTodos: () => Promise<void>;
  createTodo: (title: string, description?: string) => Promise<void>;
  updateTodo: (id: string, updates: Partial<Todo>) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
  toggleTodo: (id: string) => Promise<void>;
}

export interface UIContextType {
  currentView: string;
  showModal: boolean;
  modalType: string | null;
  modalData: any;
  notifications: Notification[];
  setCurrentView: (view: string) => void;
  setShowModal: (show: boolean) => void;
  setModalType: (type: string | null) => void;
  setModalData: (data: any) => void;
  addNotification: (message: string, type: 'success' | 'error' | 'warning' | 'info') => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

// Form validation errors
export interface ValidationError {
  field: string;
  message: string;
}