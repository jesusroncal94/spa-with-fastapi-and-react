import type { Task } from "../types";

interface TaskItemProps {
  task: Task;
  onToggle: (task: Task) => void;
  onDelete: (task: Task) => void;
}

export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className={task.done ? "task task--done" : "task"}>
      <label>
        <input type="checkbox" checked={task.done} onChange={() => onToggle(task)} />
        <span>{task.title}</span>
      </label>
      <button type="button" aria-label={`Delete ${task.title}`} onClick={() => onDelete(task)}>
        ×
      </button>
    </li>
  );
}
