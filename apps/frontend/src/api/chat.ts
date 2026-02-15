export interface ChatResponse {
    reply: string;
    model: string;
    usage?: Record<string, unknown>;
    latency?: number;
}

export interface ChatRequest {
    message: string;
    model: 'gpt-4' | 'deepseek';
    stream?: boolean;
    system_prompt?: string;
}

export interface StreamEvent {
    type: 'delta' | 'done' | 'error';
    content?: string;
    latency?: number;
    model?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const chatApi = {
    sendMessage: async (data: ChatRequest, signal?: AbortSignal): Promise<ChatResponse> => {
        const response = await fetch(`${API_BASE_URL}/chat/completions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            signal,
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API Error: ${response.status}`);
        }
        return response.json();
    },

    streamMessage: async (data: ChatRequest, onEvent: (event: StreamEvent) => void, signal?: AbortSignal): Promise<void> => {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, stream: true }),
            signal,
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Stream Error: ${response.status}`);
        }
        const reader = response.body?.getReader();
        if (!reader) throw new Error('ReadableStream not supported');
        const decoder = new TextDecoder();
        let buffer = '';
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';
            for (const line of lines) {
                const trimmed = line.trim();
                if (!trimmed.startsWith('data: ')) continue;
                const json = trimmed.slice(6);
                try { onEvent(JSON.parse(json)); } catch { onEvent({ type: 'delta', content: json }); }
            }
        }
        if (buffer.trim().startsWith('data: ')) {
            try { onEvent(JSON.parse(buffer.trim().slice(6))); } catch { /* ignore */ }
        }
    },

    checkHealth: async (): Promise<boolean> => {
        try {
            const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/health`, { signal: AbortSignal.timeout(5000) });
            return response.ok;
        } catch { return false; }
    },
};
