// API Client for backend communication
// This will handle all communication with the backend API

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

interface ApiResponse<T> {
  success?: boolean;
  data?: T;
  error?: string;
  errorCode?: string;
}

// Generic API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const url = `${API_BASE_URL}${endpoint}`;

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add authorization header if token exists
    const token = localStorage.getItem('token');
    if (token && !config.headers?.['Authorization']) {
      (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, config);

    // Handle different response status codes
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        success: false,
        error: errorData.error || `HTTP error! status: ${response.status}`,
        errorCode: errorData.errorCode
      };
    }

    const data = await response.json();
    return { data, success: true };
  } catch (error) {
    console.error('API request error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Network error occurred'
    };
  }
}

// Authentication API functions
export const authApi = {
  // User registration
  async register(email: string, password: string, name?: string) {
    return apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name })
    });
  },

  // User login
  async login(email: string, password: string) {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
  },

  // User logout
  async logout() {
    return apiRequest('/auth/logout', {
      method: 'POST'
    });
  },

  // Get current session
  async getSession() {
    return apiRequest('/auth/session');
  }
};

// Todo API functions
export const todoApi = {
  // Get user's todos
  async getTodos() {
    return apiRequest('/todos');
  },

  // Create new todo
  async createTodo(title: string, description?: string, completed: boolean = false) {
    return apiRequest('/todos', {
      method: 'POST',
      body: JSON.stringify({ title, description, completed })
    });
  },

  // Update existing todo
  async updateTodo(id: string, updates: { title?: string; description?: string; completed?: boolean }) {
    return apiRequest(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    });
  },

  // Delete todo
  async deleteTodo(id: string) {
    return apiRequest(`/todos/${id}`, {
      method: 'DELETE'
    });
  }
};

export default {
  auth: authApi,
  todos: todoApi
};