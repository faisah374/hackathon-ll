import React, { useState } from 'react';
import { useTodo } from '@/providers/todo-provider';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

const TodoForm = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const { createTodo, isCreating } = useTodo();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      setError('');
      await createTodo(title, description);
      setTitle('');
      setDescription('');
    } catch (err) {
      setError('Failed to create todo. Please try again.');
      console.error('Error creating todo:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-4">Add New Todo</h2>

      {error && (
        <div className="mb-4 text-red-500 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        <Input
          label="Title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          required
        />

        <Input
          label="Description (Optional)"
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
        />

        <Button
          type="submit"
          disabled={isCreating || !title.trim()}
          loading={isCreating}
        >
          {isCreating ? 'Adding...' : 'Add Todo'}
        </Button>
      </div>
    </form>
  );
};

export default TodoForm;