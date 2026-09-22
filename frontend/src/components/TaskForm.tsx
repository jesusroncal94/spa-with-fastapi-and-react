import { useState, type FormEvent } from "react";

interface TaskFormProps {
  onSubmit: (title: string) => Promise<void>;
}

export function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [saving, setSaving] = useState(false);

  const trimmed = title.trim();

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!trimmed || saving) {
      return;
    }

    setSaving(true);
    try {
      await onSubmit(trimmed);
      setTitle("");
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <input
        aria-label="Task title"
        placeholder="What needs doing?"
        value={title}
        maxLength={200}
        onChange={(event) => setTitle(event.target.value)}
      />
      <button type="submit" disabled={!trimmed || saving}>
        Add
      </button>
    </form>
  );
}
