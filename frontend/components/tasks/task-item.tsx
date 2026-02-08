"use client";

import { useState } from "react";
import { useSession } from "@/lib/auth-client";
import { Task, taskApi } from "@/lib/api-client";

interface TaskItemProps {
  task: Task;
  onTaskUpdated?: () => void;
  onEditTask?: (task: Task) => void;
  onDeleteTask?: (task: Task) => void;
}

export default function TaskItem({ task, onTaskUpdated, onEditTask, onDeleteTask }: TaskItemProps) {
  const { user } = useSession();
  const [isUpdating, setIsUpdating] = useState(false);
  const [localCompleted, setLocalCompleted] = useState(task.completed);
  const [error, setError] = useState<string | null>(null);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const handleToggleComplete = async () => {
    if (!user?.external_id || isUpdating) return;

    // Optimistic update
    const previousCompleted = localCompleted;
    setLocalCompleted(!localCompleted);
    setError(null);
    setIsUpdating(true);

    try {
      await taskApi.completeTask(user.external_id, task.id, !localCompleted);
      if (onTaskUpdated) {
        onTaskUpdated();
      }
    } catch (err: any) {
      // Rollback on error
      setLocalCompleted(previousCompleted);
      setError(err.detail || "Failed to update task");
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="border border-gray-200 rounded-lg p-3 sm:p-4 hover:border-gray-300 transition-colors">
      {error && (
        <div className="mb-3 text-xs text-red-600 bg-red-50 border border-red-200 rounded-md p-2">
          {error}
        </div>
      )}
      <div className="flex items-start space-x-2 sm:space-x-3">
        <div className="flex-shrink-0 mt-1">
          <button
            onClick={handleToggleComplete}
            disabled={isUpdating}
            className="w-6 h-6 sm:w-5 sm:h-5 rounded border-2 border-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center hover:border-blue-500 transition-colors touch-manipulation"
            aria-label={localCompleted ? "Mark as incomplete" : "Mark as complete"}
            aria-pressed={localCompleted}
          >
            {isUpdating ? (
              <svg
                className="w-3 h-3 text-gray-400 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            ) : localCompleted ? (
              <svg
                className="w-3 h-3 text-blue-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            ) : null}
          </button>
        </div>
        <div className="flex-1 min-w-0">
          <h3
            className={`text-sm sm:text-base font-medium transition-all break-words ${
              localCompleted
                ? "text-gray-500 line-through"
                : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-1 text-xs sm:text-sm transition-all break-words ${
                localCompleted ? "text-gray-400 line-through" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}
          <div className="mt-2 flex flex-wrap items-center text-xs text-gray-500 gap-x-2">
            <span>Created {formatDate(task.created_at)}</span>
            {task.priority && (
              <>
                <span className="hidden sm:inline">•</span>
                <span className="capitalize">{task.priority}</span>
              </>
            )}
            {localCompleted && (
              <>
                <span className="hidden sm:inline">•</span>
                <span className="text-green-600 font-medium">Completed</span>
              </>
            )}
          </div>
        </div>
        <div className="flex-shrink-0 ml-2 sm:ml-3 flex space-x-0.5 sm:space-x-1">
          <button
            onClick={() => onEditTask?.(task)}
            className="p-2 sm:p-2 min-w-[44px] min-h-[44px] sm:min-w-0 sm:min-h-0 text-gray-400 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 rounded transition-colors touch-manipulation flex items-center justify-center"
            aria-label="Edit task"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={() => onDeleteTask?.(task)}
            className="p-2 sm:p-2 min-w-[44px] min-h-[44px] sm:min-w-0 sm:min-h-0 text-gray-400 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 rounded transition-colors touch-manipulation flex items-center justify-center"
            aria-label="Delete task"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
