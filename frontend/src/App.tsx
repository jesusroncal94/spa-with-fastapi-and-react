import { useCallback, useEffect, useState } from "react";

import { createTask, deleteTask, listTasks, updateTask } from "./api";
import { TaskForm } from "./components/TaskForm";
import { TaskList } from "./components/TaskList";
import type { Task } from "./types";

export function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      setTasks(await listTasks());
      setError(null);
    } catch {
      setError("The task list could not be loaded.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function runAndRefresh(operation: () => Promise<unknown>, failure: string) {
    try {
      await operation();
      await refresh();
    } catch {
      setError(failure);
    }
  }

  const pending = tasks.filter((task) => !task.done).length;

  return (
    <main className="app">
      <header>
        <h1>Taskboard</h1>
        <p>
          {pending} pending of {tasks.length}
        </p>
      </header>

      <TaskForm
        onSubmit={(title) => runAndRefresh(() => createTask(title), "The task could not be created.")}
      />

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p className="empty">Loading…</p>
      ) : (
        <TaskList
          tasks={tasks}
          onToggle={(task) =>
            void runAndRefresh(
              () => updateTask(task.id, { done: !task.done }),
              "The task could not be updated.",
            )
          }
          onDelete={(task) =>
            void runAndRefresh(() => deleteTask(task.id), "The task could not be deleted.")
          }
        />
      )}
    </main>
  );
}
