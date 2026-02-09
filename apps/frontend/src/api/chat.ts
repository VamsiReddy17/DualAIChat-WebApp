export interface ChatResponse {
    reply: string;
}

export interface ChatRequest {
    message: string;
    model: 'gpt-4' | 'deepseek';
    stream?: boolean;
    system_prompt?: string;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const chatApi = {
    sendMessage: async (data: ChatRequest): Promise<ChatResponse> => {
        const response = await fetch(`${API_BASE_URL}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API Error: ${response.statusText}`);
        }

        return response.json();
    },

    streamMessage: async (data: ChatRequest, onChunk: (chunk: string) => void): Promise<void> => {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ...data, stream: true }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Stream Error: ${response.statusText}`);
        }

        const reader = response.body?.getReader();
        if (!reader) throw new Error('ReadableStream not supported');

        const decoder = new TextDecoder();
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            onChunk(chunk);
        }
    }
};
