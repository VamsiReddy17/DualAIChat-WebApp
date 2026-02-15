/**
 * Shared TypeScript types used across all apps.
 *
 * Import from "@dualai/shared-types" in any workspace package.
 */

// ---- Model identifiers ----
export type ModelId = 'gpt-4' | 'deepseek';
export type ViewMode = 'both' | ModelId;

// ---- Chat messages ----
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  model?: ModelId;
  timestamp: string;
  latency?: number;
  usage?: Record<string, unknown>;
  error?: boolean;
}

// ---- API contracts ----
export interface ChatRequest {
  message: string;
  model: ModelId;
  stream?: boolean;
  system_prompt?: string;
}

export interface ChatResponse {
  reply: string;
  model: string;
  usage?: Record<string, unknown>;
  latency?: number;
}

export interface StreamEvent {
  type: 'delta' | 'done' | 'error';
  content?: string;
  latency?: number;
  model?: string;
}

// ---- Session / history ----
export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt?: string;
}
