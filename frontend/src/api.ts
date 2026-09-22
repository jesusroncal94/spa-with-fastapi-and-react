import type { Task, UpdateTaskInput } from "./types";

const API_BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`The server answered ${response.status}`);
  }

  return response.status === 204 ? (undefined as T) : ((await response.json()) as T);
}

export const listTasks = () => request<Task[]>("/tasks");

export const createTask = (title: string) =>
  request<Task>("/tasks", { method: "POST", body: JSON.stringify({ title }) });

export const updateTask = (id: string, changes: UpdateTaskInput) =>
  request<Task>(`/tasks/${id}`, { method: "PATCH", body: JSON.stringify(changes) });

export const deleteTask = (id: string) => request<void>(`/tasks/${id}`, { method: "DELETE" });
