"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import { taskApi, Task } from "@/lib/api-client";
import TaskList from "./task-list";
import LoadingSkeleton from "./loading-skeleton";
import ErrorMessage from "./error-message";
import CreateTaskForm from "./create-task-form";
import EditTaskModal from "./edit-task-modal";
import DeleteConfirmationDialog from "./delete-confirmation";

export default function TaskDashboard() {
  const router = useRouter();
  const { user } = useSession();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [isSigningOut, setIsSigningOut] = useState(false);

  const fetchTasks = async () => {
    if (!user?.external_id) return;

    setIsLoading(true);
    setError(null);

    try {
      const fetchedTasks = await taskApi.getTasks(user.external_id);
      setTasks(fetchedTasks);
    } catch (err: any) {
      setError(err.detail || "Failed to load tasks. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [user?.external_id]);

  const handleTaskCreated = () => {
    setShowCreateForm(false);
    fetchTasks();
  };

  const handleTaskUpdated = () => {
    setEditingTask(null);
    fetchTasks();
  };

  const handleTaskDeleted = () => {
    setDeletingTask(null);
    fetchTasks();
  };

  const handleSignOut = async () => {
    setIsSigningOut(true);
    try {
      await signOut();
      router.push("/");
    } catch (err) {
      console.error("Sign out error:", err);
      setIsSigningOut(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="px-4 sm:px-6 py-4 sm:py-5 border-b border-gray-200">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div className="min-w-0 flex-1">
                <h1 className="text-xl sm:text-2xl font-bold text-gray-900 truncate">My Tasks</h1>
                <p className="mt-1 text-xs sm:text-sm text-gray-500 truncate">
                  {user?.email}
                </p>
              </div>
              <div className="flex gap-2 sm:gap-3">
                {!showCreateForm && (
                  <button
                    onClick={() => setShowCreateForm(true)}
                    className="flex-1 sm:flex-none inline-flex items-center justify-center px-4 py-2.5 sm:py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 min-h-[44px] sm:min-h-0 whitespace-nowrap"
                  >
                    <svg
                      className="-ml-1 mr-2 h-5 w-5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                      aria-hidden="true"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                        clipRule="evenodd"
                      />
                    </svg>
                    New Task
                  </button>
                )}
                <button
                  onClick={handleSignOut}
                  disabled={isSigningOut}
                  className="inline-flex items-center justify-center px-4 py-2.5 sm:py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed min-h-[44px] sm:min-h-0 whitespace-nowrap"
                >
                  <svg
                    className="-ml-1 mr-2 h-5 w-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                    />
                  </svg>
                  {isSigningOut ? "Signing out..." : "Sign Out"}
                </button>
              </div>
            </div>
          </div>

          <div className="px-4 sm:px-6 py-4 sm:py-6">
            {showCreateForm && (
              <CreateTaskForm
                onTaskCreated={handleTaskCreated}
                onCancel={() => setShowCreateForm(false)}
              />
            )}

            {isLoading ? (
              <LoadingSkeleton />
            ) : error ? (
              <ErrorMessage message={error} onRetry={fetchTasks} />
            ) : (
              <TaskList
                tasks={tasks}
                onCreateTask={() => setShowCreateForm(true)}
                onTaskUpdated={fetchTasks}
                onEditTask={setEditingTask}
                onDeleteTask={setDeletingTask}
              />
            )}
          </div>
        </div>
      </div>

      {editingTask && (
        <EditTaskModal
          task={editingTask}
          onClose={() => setEditingTask(null)}
          onTaskUpdated={handleTaskUpdated}
        />
      )}

      {deletingTask && (
        <DeleteConfirmationDialog
          task={deletingTask}
          onClose={() => setDeletingTask(null)}
          onTaskDeleted={handleTaskDeleted}
        />
      )}
    </div>
  );
}
