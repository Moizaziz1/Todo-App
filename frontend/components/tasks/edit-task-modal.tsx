"use client";

import { useState, useEffect } from "react";
import { useSession } from "@/lib/auth-client";
import { Task, taskApi, UpdateTaskInput } from "@/lib/api-client";

interface EditTaskModalProps {
  task: Task;
  onClose: () => void;
  onTaskUpdated: () => void;
}

export default function EditTaskModal({
  task,
  onClose,
  onTaskUpdated,
}: EditTaskModalProps) {
  const { user } = useSession();
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Pre-fill form with current task data
    setTitle(task.title);
    setDescription(task.description || "");
  }, [task]);

  const validateForm = (): string | null => {
    if (!title.trim()) {
      return "Title is required";
    }
    if (title.length > 200) {
      return "Title must be 200 characters or less";
    }
    if (description.length > 1000) {
      return "Description must be 1000 characters or less";
    }
    return null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationError = validateForm();
    if (validationError) {
      setError(validationError);
      return;
    }

    if (!user?.external_id) {
      setError("You must be logged in to edit a task");
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const updateData: UpdateTaskInput = {
        title: title.trim(),
        description: description.trim() || undefined,
      };

      await taskApi.updateTask(user.external_id, task.id, updateData);
      onTaskUpdated();
      onClose();
    } catch (err: any) {
      setError(err.detail || "Failed to update task. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3 sm:p-4 z-50"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="edit-task-title"
    >
      <div
        className="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
          <h2 id="edit-task-title" className="text-lg sm:text-xl font-bold text-gray-900">
            Edit Task
          </h2>
        </div>

        <form onSubmit={handleSubmit} className="px-4 sm:px-6 py-3 sm:py-4">
          <div className="space-y-3 sm:space-y-4">
            <div>
              <label
                htmlFor="edit-task-title-input"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Title <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="edit-task-title-input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-3 py-2.5 sm:py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base sm:text-sm"
                placeholder="Enter task title"
                maxLength={200}
                disabled={isSubmitting}
                aria-required="true"
                aria-invalid={error ? "true" : "false"}
              />
              <p className="mt-1 text-xs text-gray-500">
                {title.length}/200 characters
              </p>
            </div>

            <div>
              <label
                htmlFor="edit-task-description"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Description
              </label>
              <textarea
                id="edit-task-description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={4}
                className="w-full px-3 py-2.5 sm:py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base sm:text-sm"
                placeholder="Enter task description (optional)"
                maxLength={1000}
                disabled={isSubmitting}
              />
              <p className="mt-1 text-xs text-gray-500">
                {description.length}/1000 characters
              </p>
            </div>

            {error && (
              <div
                className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-3"
                role="alert"
              >
                {error}
              </div>
            )}
          </div>

          <div className="mt-4 sm:mt-6 flex flex-col-reverse sm:flex-row sm:justify-end gap-2 sm:gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="w-full sm:w-auto px-4 py-2.5 sm:py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] sm:min-h-0"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full sm:w-auto px-4 py-2.5 sm:py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] sm:min-h-0"
            >
              {isSubmitting ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
