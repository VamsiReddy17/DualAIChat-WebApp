import { useState, useCallback, useRef, useEffect } from "react";
import { chatApi, type StreamEvent } from "@/api/chat";

export interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    model?: "gpt-4" | "deepseek";
    timestamp: string;
    latency?: number;
    usage?: Record<string, unknown>;
    error?: boolean;
}

let messageCounter = 0;
const generateId = () => `msg-${Date.now()}-${++messageCounter}`;

export const useChat = (selectedModel: "both" | "gpt-4" | "deepseek") => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [loadingModels, setLoadingModels] = useState<Set<string>>(new Set());
    const [systemPrompt, setSystemPrompt] = useState("You are a helpful assistant.");
    const abortRef = useRef<AbortController | null>(null);

    const isLoading = loadingModels.size > 0;

    useEffect(() => () => { abortRef.current?.abort(); }, []);

    const cancelRequest = useCallback(() => {
        abortRef.current?.abort();
        abortRef.current = null;
        setLoadingModels(new Set());
    }, []);

    const updateMsg = useCallback((id: string, fn: (m: Message) => Message) => {
        setMessages(prev => prev.map(m => m.id === id ? fn(m) : m));
    }, []);

    const sendMessage = useCallback(async (text: string) => {
        if (!text.trim() || isLoading) return;
        abortRef.current?.abort();
        const ctrl = new AbortController();
        abortRef.current = ctrl;

        const ts = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        const userMsg: Message = { id: generateId(), role: "user", content: text, timestamp: ts };
        const models: Array<"gpt-4" | "deepseek"> = selectedModel === "both" ? ["gpt-4", "deepseek"] : [selectedModel];
        const aiMsgs: Message[] = models.map(m => ({ id: generateId(), role: "assistant" as const, content: "", model: m, timestamp: ts }));
        const idMap = new Map(models.map((m, i) => [m, aiMsgs[i].id]));

        setMessages(prev => [...prev, userMsg, ...aiMsgs]);
        setLoadingModels(new Set(models));

        await Promise.all(models.map(async (model) => {
            const mid = idMap.get(model)!;
            try {
                await chatApi.streamMessage(
                    { message: text, model, system_prompt: systemPrompt },
                    (ev: StreamEvent) => {
                        if (ev.type === "delta" && ev.content) updateMsg(mid, m => ({ ...m, content: m.content + ev.content }));
                        else if (ev.type === "done") updateMsg(mid, m => ({ ...m, latency: ev.latency }));
                        else if (ev.type === "error") updateMsg(mid, m => ({ ...m, content: ev.content || "Error", error: true }));
                    },
                    ctrl.signal,
                );
            } catch (err: unknown) {
                if (err instanceof DOMException && err.name === "AbortError") return;
                const msg = err instanceof Error ? err.message : "An error occurred";
                updateMsg(mid, m => ({ ...m, content: m.content || `Error: ${msg}`, error: !m.content }));
            } finally {
                setLoadingModels(prev => { const n = new Set(prev); n.delete(model); return n; });
            }
        }));
        abortRef.current = null;
    }, [selectedModel, isLoading, systemPrompt, updateMsg]);

    const retryMessage = useCallback(async (messageId: string) => {
        const idx = messages.findIndex(m => m.id === messageId);
        if (idx === -1) return;
        const failed = messages[idx];
        if (!failed.model) return;
        let userText = "";
        for (let i = idx - 1; i >= 0; i--) { if (messages[i].role === "user") { userText = messages[i].content; break; } }
        if (!userText) return;

        const ctrl = new AbortController();
        abortRef.current = ctrl;
        const model = failed.model;
        updateMsg(messageId, m => ({ ...m, content: "", error: false }));
        setLoadingModels(new Set([model]));

        try {
            await chatApi.streamMessage(
                { message: userText, model, system_prompt: systemPrompt },
                (ev: StreamEvent) => {
                    if (ev.type === "delta" && ev.content) updateMsg(messageId, m => ({ ...m, content: m.content + ev.content }));
                    else if (ev.type === "done") updateMsg(messageId, m => ({ ...m, latency: ev.latency }));
                    else if (ev.type === "error") updateMsg(messageId, m => ({ ...m, content: ev.content || "Error", error: true }));
                },
                ctrl.signal,
            );
        } catch (err: unknown) {
            if (!(err instanceof DOMException && err.name === "AbortError")) {
                const msg = err instanceof Error ? err.message : "Error";
                updateMsg(messageId, m => ({ ...m, content: m.content || `Error: ${msg}`, error: !m.content }));
            }
        } finally {
            setLoadingModels(new Set());
            abortRef.current = null;
        }
    }, [messages, systemPrompt, updateMsg]);

    return { messages, setMessages, isLoading, loadingModels, sendMessage, cancelRequest, retryMessage, systemPrompt, setSystemPrompt };
};
