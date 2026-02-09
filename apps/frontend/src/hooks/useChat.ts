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
    const [systemPrompt, setSystemPrompt] = useState("You are a helpful assistant.");

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
                await chatApi.streamMessage({ 
                    message: text, 
                    model: model as any,
                    system_prompt: systemPrompt 
                }, (chunk) => {
                    setMessages(prev => {
                        const newMessages = [...prev];
                        // Using reverse and findIndex as a fallback for findLastIndex in older TS environments
                        const reversedIdx = [...newMessages].reverse().findIndex((m: Message) => m.model === model);
                        const idx = reversedIdx !== -1 ? newMessages.length - 1 - reversedIdx : -1;
                        
                        if (idx !== -1) {
                            if (chunk.includes("--METADATA--")) {
                                const parts = chunk.split("--METADATA--");
                                newMessages[idx].content += parts[0];
                                try {
                                    const meta = JSON.parse(parts[1].trim());
                                    newMessages[idx].latency = meta.latency;
                                } catch (e) {}
                            } else {
                                newMessages[idx].content += chunk;
                            }
                        }
                        return newMessages;
                    });
                });
            } catch (err: any) {
                setMessages(prev => {
                    const newMessages = [...prev];
                    const reversedIdx = [...newMessages].reverse().findIndex((m: Message) => m.model === model);
                    const idx = reversedIdx !== -1 ? newMessages.length - 1 - reversedIdx : -1;
                    if (idx !== -1) newMessages[idx].content = `Error: ${err.message}`;
                    return newMessages;
                });
            }
        });

        await Promise.all(streamPromises);
        setIsLoading(false);
    }, [selectedModel, isLoading, systemPrompt]);

    return { messages, setMessages, isLoading, sendMessage, systemPrompt, setSystemPrompt };
};
