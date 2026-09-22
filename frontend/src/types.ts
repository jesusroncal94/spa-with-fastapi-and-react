export interface Task {
  id: string;
  title: string;
  done: boolean;
  created_at: string;
}

export interface UpdateTaskInput {
  title?: string;
  done?: boolean;
}
