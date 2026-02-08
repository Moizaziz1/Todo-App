import { Task } from "@/lib/api-client";
import TaskItem from "./task-item";
import EmptyState from "./empty-state";

interface TaskListProps {
  tasks: Task[];
  onCreateTask?: () => void;
  onTaskUpdated?: () => void;
  onEditTask?: (task: Task) => void;
  onDeleteTask?: (task: Task) => void;
}

export default function TaskList({ tasks, onCreateTask, onTaskUpdated, onEditTask, onDeleteTask }: TaskListProps) {
  if (tasks.length === 0) {
    return <EmptyState onCreateTask={onCreateTask} />;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onTaskUpdated={onTaskUpdated}
          onEditTask={onEditTask}
          onDeleteTask={onDeleteTask}
        />
      ))}
    </div>
  );
}
