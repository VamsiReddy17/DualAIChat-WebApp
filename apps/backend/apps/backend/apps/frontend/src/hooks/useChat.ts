import { useState, useCallback } from "react";
import { chatApi } from "@/api/chat";

export interface Message {
    role: "user" | "assistant";
    content: string;
    model?: "gpt-4" | "deepseek";
    timestamp: string;
    latency?: number;
    usage?: any;
}

export const useChat = (selectedModel: "both" | "gpt-4" | "deepseek") => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = useCallback(async (text: string) => {
        if (!text.trim() || isLoading) return;

        const timestamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        const userMessage: Message = { role: "user", content: text, timestamp };

        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        const modelsToCall = selectedModel === "both" ? ["gpt-4", "deepseek"] : [selectedModel];
        
        const initialAIMessages = modelsToCall.map(m => ({
            role: "assistant" as const,
            content: "",
            model: m as "gpt-4" | "deepseek",
            timestamp
        }));
        
        setMessages(prev => [...prev, ...initialAIMessages]);

        const streamPromises = modelsToCall.map(async (model) => {
            try {
                await chatApi.streamMessage({ message: text, model: model as any }, (chunk) => {
                    setMessages(prev => {
                        const newMessages = [...prev];
                        const idx = newMessages.findLastIndex(m => m.model === model);
                        if (idx !== -1) {
                            try {
                                if (chunk.startsWith("{")) {
                                    const data = JSON.parse(chunk);
                                    newMessages[idx].content += data.reply || "";
                                    if (data.latency) newMessages[idx].latency = data.latency;
                                    if (data.usage) newMessages[idx].usage = data.usage;
                                } else {
                                    newMessages[idx].content += chunk;
                                }
                            } catch {
                                newMessages[idx].content += chunk;
                            }
                        }
                        return newMessages;
                    });
                });
            } catch (err: any) {
                setMessages(prev => {
                    const newMessages = [...prev];
                    const idx = newMessages.findLastIndex(m => m.model === model);
                    if (idx !== -1) newMessages[idx].content = `Error: ${err.message}`;
                    return newMessages;
                });
            }
        });

        await Promise.all(streamPromises);
        setIsLoading(false);
    }, [selectedModel, isLoading]);

    return { messages, setMessages, isLoading, sendMessage };
};