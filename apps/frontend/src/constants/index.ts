/**
 * Application-wide constants for the Dual AI Chat frontend.
 */

export const APP_NAME = 'Dual AI Chat';
export const APP_SUBTITLE = 'Enterprise Edition';

export const MODELS = {
  GPT4: {
    id: 'gpt-4' as const,
    label: 'GPT-4o',
    provider: 'Azure OpenAI',
    description: 'Fast & Versatile',
  },
  DEEPSEEK: {
    id: 'deepseek' as const,
    label: 'DeepSeek-R1',
    provider: 'Azure AI Foundry',
    description: 'Reasoning',
  },
} as const;

export const SUGGESTED_PROMPTS = [
  { label: 'Explain quantum computing', icon: '\u{1F52C}' },
  { label: 'Write a Python REST API', icon: '\u{1F40D}' },
  { label: 'Compare cloud providers', icon: '\u{2601}\u{FE0F}' },
  { label: 'Design a database schema', icon: '\u{1F5C4}\u{FE0F}' },
] as const;

export const API_BASE_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const HEALTH_CHECK_INTERVAL_MS = 30_000;
export const MESSAGE_MAX_LENGTH = 32_000;
export const SYSTEM_PROMPT_MAX_LENGTH = 4_000;
export const DEFAULT_SYSTEM_PROMPT = 'You are a helpful assistant.';
