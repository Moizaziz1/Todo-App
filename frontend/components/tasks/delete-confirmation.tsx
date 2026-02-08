"use client";

import { useState } from "react";
import { useSession } from "@/lib/auth-client";
import { Task, taskApi } from "@/lib/api-client";

interface DeleteConfirmationDialogProps {
  task: Task;
  onClose: () => void;
  onTaskDeleted: () => void;
}

export default function DeleteConfirmationDialog({
  task,
  onClose,
  onTaskDeleted,
}: DeleteConfirmationDialogProps) {
  const { user } = useSession();
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async () => {
    if (!user?.external_id) {
      setError("You must be logged in to delete a task");
      return;
    }

    setIsDeleting(true);
    setError(null);

    try {
      await taskApi.deleteTask(user.external_id, task.id);
      onTaskDeleted();
      onClose();
    } catch (err: any) {
      setError(err.detail || "Failed to delete task. Please try again.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3 sm:p-4 z-50"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-task-title"
    >
      <div
        className="bg-white rounded-lg shadow-xl max-w-md w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-4 sm:px-6 py-3 sm:py-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg
                className="h-6 w-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <div className="ml-3 flex-1">
              <h3
                id="delete-task-title"
                className="text-lg font-medium text-gray-900"
              >
                Delete Task
              </h3>
              <div className="mt-2">
                <p className="text-sm text-gray-500">
                  Are you sure you want to delete "{task.title}"? This action
                  cannot be undone.
                </p>
              </div>
              {error && (
                <div
                  className="mt-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-3"
                  role="alert"
                >
                  {error}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="bg-gray-50 px-4 sm:px-6 py-2 sm:py-3 flex flex-col-reverse sm:flex-row sm:justify-end gap-2 sm:gap-3 rounded-b-lg">
          <button
            type="button"
            onClick={onClose}
            disabled={isDeleting}
            className="w-full sm:w-auto px-4 py-2.5 sm:py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] sm:min-h-0"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleDelete}
            disabled={isDeleting}
            className="w-full sm:w-auto px-4 py-2.5 sm:py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] sm:min-h-0"
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}
