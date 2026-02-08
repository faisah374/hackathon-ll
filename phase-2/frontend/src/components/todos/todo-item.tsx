import React, { useState } from 'react';
import { Todo } from '@/lib/types';
import { useTodo } from '@/providers/todo-provider';
import { Button } from '@/components/ui/button';

interface TodoItemProps {
  todo: Todo;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo }) => {
  const { toggleTodo, updateTodo, deleteTodo } = useTodo();
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');

  const handleToggle = async () => {
    await toggleTodo(todo.id);
  };

  const handleEdit = async () => {
    try {
      await updateTodo(todo.id, {
        title: editTitle,
        description: editDescription
      });
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await deleteTodo(todo.id);
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    }
  };

  return (
    <div className={`border rounded-lg p-4 flex items-start ${todo.completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
        <div className="flex-1 space-y-3">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full border rounded px-2 py-1 mb-2"
            autoFocus
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full border rounded px-2 py-1 mb-2"
            rows={2}
          />
          <div className="flex space-x-2">
            <Button size="sm" onClick={handleEdit}>Save</Button>
            <Button size="sm" variant="outline" onClick={() => setIsEditing(false)}>Cancel</Button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start flex-1">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggle}
              className="mt-1 mr-3 h-5 w-5"
            />
            <div className="flex-1">
              <h3 className={`text-lg ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {todo.title}
              </h3>
              {todo.description && (
                <p className={`mt-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                  {todo.description}
                </p>
              )}
              <p className="text-xs text-gray-500 mt-2">
                Created: {new Date(todo.createdAt).toLocaleDateString()}
                {todo.updatedAt !== todo.createdAt && (
                  <span>, Updated: {new Date(todo.updatedAt).toLocaleDateString()}</span>
                )}
              </p>
            </div>
          </div>
          <div className="flex space-x-2 ml-4">
            <Button size="sm" variant="outline" onClick={() => setIsEditing(true)}>
              Edit
            </Button>
            <Button size="sm" variant="outline" onClick={handleDelete}>
              Delete
            </Button>
          </div>
        </>
      )}
    </div>
  );
};

export default TodoItem;