'use client';

import { createContext, useContext, useState, ReactNode, useCallback } from 'react';

// Define types
interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  timestamp: number;
}

interface UIContextType {
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

// Create context
const UIContext = createContext<UIContextType | undefined>(undefined);

// UIProvider component
export function UIProvider({ children }: { children: ReactNode }) {
  const [currentView, setCurrentView] = useState<string>('dashboard'); // Default view
  const [showModal, setShowModal] = useState<boolean>(false);
  const [modalType, setModalType] = useState<string | null>(null);
  const [modalData, setModalData] = useState<any>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback((message: string, type: 'success' | 'error' | 'warning' | 'info') => {
    const newNotification: Notification = {
      id: Date.now().toString(),
      message,
      type,
      timestamp: Date.now()
    };

    setNotifications(prev => [...prev, newNotification]);

    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      removeNotification(newNotification.id);
    }, 5000);
  }, []);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const clearNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  const value: UIContextType = {
    currentView,
    showModal,
    modalType,
    modalData,
    notifications,
    setCurrentView,
    setShowModal,
    setModalType,
    setModalData,
    addNotification,
    removeNotification,
    clearNotifications
  };

  return (
    <UIContext.Provider value={value}>
      {children}
    </UIContext.Provider>
  );
}

// Custom hook to use UI context
export function useUI() {
  const context = useContext(UIContext);
  if (context === undefined) {
    throw new Error('useUI must be used within a UIProvider');
  }
  return context;
}