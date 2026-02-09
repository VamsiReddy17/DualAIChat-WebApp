import React, { useState, useEffect, useRef } from 'react';
import { Send, BrainCircuit, Zap, RefreshCw, LayoutGrid, Sparkles, MessageSquare, Info, History, Plus, Trash2, Settings2, Terminal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { ThemeToggle } from '@/components/ThemeToggle';
import { MessageBubble } from '@/components/MessageBubble';
import { motion, AnimatePresence } from 'framer-motion';
import { useChat, type Message } from '@/hooks/useChat';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";

const SUGGESTED_PROMPTS = [
    "Explain quantum computing in simple terms",
    "Write a Python script to scrape a website",
    "Compare React and Vue for a new project",
    "Give me 5 healthy breakfast ideas"
];

export const ChatWindow = () => {
    const [selectedModel, setSelectedModel] = useState<'both' | 'gpt-4' | 'deepseek'>('both');
    const { messages, setMessages, isLoading, sendMessage, systemPrompt, setSystemPrompt } = useChat(selectedModel);
    const [input, setInput] = useState('');
    const [history, setHistory] = useState<{id: string, title: string, messages: Message[]}[]>([]);
    const [currentChatId, setCurrentChatId] = useState<string | null>(null);
    const scrollAreaRefGPT = useRef<HTMLDivElement>(null);
    const scrollAreaRefDeepSeek = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const savedHistory = localStorage.getItem('chat_history');
        if (savedHistory) setHistory(JSON.parse(savedHistory));
    }, []);

    useEffect(() => {
        if (history.length > 0) localStorage.setItem('chat_history', JSON.stringify(history));
    }, [history]);

    const scrollToBottom = (ref: React.RefObject<HTMLDivElement | null>) => {
        if (ref.current) {
            const scrollContainer = ref.current.querySelector('[data-radix-scroll-area-viewport]');
            if (scrollContainer) {
                scrollContainer.scrollTo({ top: scrollContainer.scrollHeight, behavior: 'smooth' });
            }
        }
    };

    useEffect(() => {
        scrollToBottom(scrollAreaRefGPT);
        scrollToBottom(scrollAreaRefDeepSeek);
    }, [messages, isLoading]);

    const handleSend = async (text: string = input) => {
        if (!text.trim() || isLoading) return;
        setInput('');
        await sendMessage(text);
    };

    const startNewChat = () => {
        if (messages.length > 0) {
            const newChat = {
                id: Date.now().toString(),
                title: messages[0].content.slice(0, 30) + '...',
                messages: messages
            };
            setHistory(prev => [newChat, ...prev]);
        }
        setMessages([]);
        setCurrentChatId(null);
    };

    const loadChat = (chat: {id: string, title: string, messages: Message[]}) => {
        setMessages(chat.messages);
        setCurrentChatId(chat.id);
    };

    return (
        <div className="flex flex-col h-screen w-full bg-background text-foreground overflow-hidden transition-colors duration-500">
            <header className="flex-none h-16 border-b border-border/40 bg-background/60 backdrop-blur-xl flex items-center justify-between px-6 z-30 sticky top-0">
                <div className="flex items-center gap-3">
                    <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-xl shadow-lg shadow-purple-500/20">
                        <Zap className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex flex-col">
                        <h1 className="font-bold text-lg leading-tight tracking-tight">Dual AI Chat</h1>
                        <span className="text-[10px] text-muted-foreground font-medium uppercase tracking-widest">v2.1 • Pro Edition</span>
                    </div>
                </div>
                
                <div className="hidden md:flex items-center bg-muted/50 p-1 rounded-lg border border-border/50">
                    <Button variant={selectedModel === 'both' ? 'secondary' : 'ghost'} size="sm" className="h-8 text-xs px-3" onClick={() => setSelectedModel('both')}>
                        <LayoutGrid className="w-3.5 h-3.5 mr-1.5" /> Dual View
                    </Button>
                    <Button variant={selectedModel === 'gpt-4' ? 'secondary' : 'ghost'} size="sm" className="h-8 text-xs px-3" onClick={() => setSelectedModel('gpt-4')}>
                        <Sparkles className="w-3.5 h-3.5 mr-1.5 text-blue-500" /> GPT-4o
                    </Button>
                    <Button variant={selectedModel === 'deepseek' ? 'secondary' : 'ghost'} size="sm" className="h-8 text-xs px-3" onClick={() => setSelectedModel('deepseek')}>
                        <BrainCircuit className="w-3.5 h-3.5 mr-1.5 text-purple-500" /> DeepSeek
                    </Button>
                </div>

                <div className="flex items-center gap-3">
                    <Sheet>
                        <SheetTrigger asChild>
                            <Button variant="outline" size="icon" className="h-9 w-9"><History className="w-4 h-4" /></Button>
                        </SheetTrigger>
                        <SheetContent side="left" className="w-[300px] sm:w-[400px]">
                            <SheetHeader>
                                <SheetTitle className="flex items-center gap-2"><History className="w-5 h-5" /> Chat History</SheetTitle>
                            </SheetHeader>
                            <div className="mt-6 flex flex-col gap-2">
                                <Button onClick={startNewChat} className="w-full justify-start gap-2" variant="outline"><Plus className="w-4 h-4" /> New Chat</Button>
                                <ScrollArea className="h-[calc(100vh-180px)] mt-4">
                                    <div className="flex flex-col gap-2 pr-4">
                                        {history.map((chat) => (
                                            <div key={chat.id} className="group flex items-center gap-2">
                                                <Button variant={currentChatId === chat.id ? "secondary" : "ghost"} className="flex-1 justify-start text-left truncate font-normal" onClick={() => loadChat(chat)}>
                                                    <MessageSquare className="w-4 h-4 mr-2 shrink-0 opacity-50" />
                                                    <span className="truncate">{chat.title}</span>
                                                </Button>
                                                <Button variant="ghost" size="icon" className="h-8 w-8 opacity-0 group-hover:opacity-100 text-destructive hover:text-destructive hover:bg-destructive/10" onClick={() => setHistory(prev => prev.filter(h => h.id !== chat.id))}>
                                                    <Trash2 className="w-3.5 h-3.5" />
                                                </Button>
                                            </div>
                                        ))}
                                    </div>
                                </ScrollArea>
                            </div>
                        </SheetContent>
                    </Sheet>
                    <ThemeToggle />
                    <Button variant="outline" size="sm" className="h-9 px-3 text-muted-foreground hover:text-foreground" onClick={startNewChat}>
                        <RefreshCw className="w-3.5 h-3.5 mr-2" /> Clear
                    </Button>
                </div>
            </header>

            <div className="flex-1 flex flex-col md:flex-row overflow-hidden p-3 md:p-4 gap-3 md:gap-4 relative">
                {(selectedModel === 'both' || selectedModel === 'gpt-4') && (
                    <Card className={cn("flex-1 flex flex-col h-full border-border/50 bg-card/30 backdrop-blur-sm shadow-xl overflow-hidden transition-all duration-500", selectedModel === 'gpt-4' ? "max-w-4xl mx-auto" : "", selectedModel === 'both' ? "h-[50%] md:h-full" : "h-full")}>
                        <CardHeader className="flex-none py-3 px-5 border-b border-border/50 bg-muted/30">
                            <CardTitle className="flex items-center justify-between">
                                <div className="flex items-center gap-2.5 text-blue-600 dark:text-blue-400">
                                    <Sparkles className="w-4 h-4" />
                                    <div className="flex flex-col">
                                        <span className="font-bold text-sm">GPT-4o</span>
                                        <span className="text-[9px] font-medium opacity-60 uppercase tracking-tighter">OpenAI Intelligence</span>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2">
                                    {messages.some(m => m.model === 'gpt-4' && m.latency) && (
                                        <div className="text-[10px] font-mono text-muted-foreground/60 bg-muted/50 px-2 py-0.5 rounded-full">
                                            {messages.filter(m => m.model === 'gpt-4').pop()?.latency?.toFixed(2)}s
                                        </div>
                                    )}
                                    <Info className="w-3.5 h-3.5 text-muted-foreground/50 cursor-help" />
                                </div>
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 p-0 min-h-0 relative">
                            <ScrollArea className="h-full p-4 md:p-5" ref={scrollAreaRefGPT}>
                                <div className="space-y-6 pb-4">
                                    <AnimatePresence initial={false}>
                                        {messages.length === 0 ? (
                                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center h-full min-h-[200px] text-center opacity-40">
                                                <div className="w-12 h-12 md:w-16 md:h-16 rounded-full bg-blue-500/10 flex items-center justify-center mb-4"><Sparkles className="w-6 h-6 md:w-8 md:h-8 text-blue-500" /></div>
                                                <p className="text-sm font-medium">GPT-4o is ready</p>
                                            </motion.div>
                                        ) : (
                                            messages.filter(m => m.role === 'user' || m.model === 'gpt-4').map((msg, idx) => (
                                                <MessageBubble key={idx} msg={msg} isUser={msg.role === 'user'} />
                                            ))
                                        )}
                                    </AnimatePresence>
                                    {isLoading && (selectedModel === 'both' || selectedModel === 'gpt-4') && (
                                        <div className="flex items-center gap-2 text-[10px] font-bold text-blue-500/60 ml-12 uppercase tracking-widest animate-pulse">
                                            <div className="flex gap-1">
                                                <span className="w-1 h-1 bg-current rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                                <span className="w-1 h-1 bg-current rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                                <span className="w-1 h-1 bg-current rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                            </div> Generating
                                        </div>
                                    )}
                                </div>
                            </ScrollArea>
                        </CardContent>
                    </Card>
                )}

                {selectedModel === 'both' && <div className="hidden md:block w-px bg-border/20 self-stretch my-10" />}

                {(selectedModel === 'both' || selectedModel === 'deepseek') && (
                    <Card className={cn("flex-1 flex flex-col h-full border-border/50 bg-card/30 backdrop-blur-sm shadow-xl overflow-hidden transition-all duration-500", selectedModel === 'deepseek' ? "max-w-4xl mx-auto" : "", selectedModel === 'both' ? "h-[50%] md:h-full" : "h-full")}>
                        <CardHeader className="flex-none py-3 px-5 border-b border-border/50 bg-muted/30">
                            <CardTitle className="flex items-center justify-between">
                                <div className="flex items-center gap-2.5 text-purple-600 dark:text-purple-400">
                                    <BrainCircuit className="w-4 h-4" />
                                    <div className="flex flex-col">
                                        <span className="font-bold text-sm">DeepSeek-V3</span>
                                        <span className="text-[9px] font-medium opacity-60 uppercase tracking-tighter">High Performance Reasoning</span>
                                    </div>
                                </div>
                                <div className="flex items-center gap-2">
                                    {messages.some(m => m.model === 'deepseek' && m.latency) && (
                                        <div className="text-[10px] font-mono text-muted-foreground/60 bg-muted/50 px-2 py-0.5 rounded-full">
                                            {messages.filter(m => m.model === 'deepseek').pop()?.latency?.toFixed(2)}s
                                        </div>
                                    )}
                                    <Info className="w-3.5 h-3.5 text-muted-foreground/50 cursor-help" />
                                </div>
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="flex-1 p-0 min-h-0 relative">
                            <ScrollArea className="h-full p-4 md:p-5" ref={scrollAreaRefDeepSeek}>
                                <div className="space-y-6 pb-4">
                                    <AnimatePresence initial={false}>
                                        {messages.length === 0 ? (
                                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col items-center justify-center h-full min-h-[200px] text-center opacity-40">
                                                <div className="w-12 h-12 md:w-16 md:h-16 rounded-full bg-purple-500/10 flex items-center justify-center mb-4"><BrainCircuit className="w-8 h-8 text-purple-500" /></div>
                                                <p className="text-sm font-medium">DeepSeek is active</p>
                                            </motion.div>
                                        ) : (
                                            messages.filter(m => m.role === 'user' || m.model === 'deepseek').map((msg, idx) => (
                                                <MessageBubble key={idx} msg={msg} isUser={msg.role === 'user'} />
                                            ))
                                        )}
                                    </AnimatePresence>
                                    {isLoading && (selectedModel === 'both' || selectedModel === 'deepseek') && (
                                        <div className="flex items-center gap-2 text-[10px] font-bold text-purple-500/60 ml-12 uppercase tracking-widest animate-pulse">
                                            <div className="flex gap-1">
                                                <span className="w-1 h-1 bg-current rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                                <span className="w-1 h-1 bg-current rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                                <span className="w-1 h-1 bg-current rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                            </div> Reasoning
                                        </div>
                                    )}
                                </div>
                            </ScrollArea>
                        </CardContent>
                    </Card>
                )}
            </div>

            <div className="flex-none p-4 md:p-6 pt-2 bg-gradient-to-t from-background via-background to-transparent z-20">
                <div className="max-w-4xl mx-auto flex flex-col gap-4">
                    {messages.length === 0 && (
                        <div className="flex flex-wrap justify-center gap-2 mb-2">
                            {SUGGESTED_PROMPTS.map((prompt, i) => (
                                <Button key={i} variant="outline" size="sm" className="text-[11px] h-8 bg-card/50 border-border/40 hover:bg-muted transition-all" onClick={() => handleSend(prompt)} disabled={isLoading}>
                                    <MessageSquare className="w-3 h-3 mr-1.5 opacity-50" /> {prompt}
                                </Button>
                            ))}
                        </div>
                    )}

                    <div className="relative group">
                        <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl opacity-10 group-hover:opacity-20 blur transition duration-500"></div>
                        <div className="relative flex items-center bg-card/80 backdrop-blur-2xl border border-border/40 rounded-2xl shadow-2xl p-2 pr-2">
                            <Input placeholder={selectedModel === 'both' ? "Ask both models..." : `Ask ${selectedModel === 'gpt-4' ? 'GPT-4o' : 'DeepSeek'}...`} className="flex-1 bg-transparent border-none focus-visible:ring-0 text-base px-4 h-12 placeholder:text-muted-foreground/40" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()} disabled={isLoading} autoFocus />
                            <Button size="icon" onClick={() => handleSend()} disabled={isLoading || !input.trim()} className={cn("h-10 w-10 rounded-xl transition-all duration-300", input.trim() ? "bg-gradient-to-br from-blue-600 to-purple-600 hover:shadow-lg hover:shadow-purple-500/25" : "bg-muted text-muted-foreground")}>
                                <Send className="w-4 h-4" />
                            </Button>
                        </div>
                    </div>
                    <div className="flex items-center justify-between px-2">
                        <div className="flex items-center gap-4 text-[9px] text-muted-foreground/50 uppercase tracking-[0.2em] font-bold">
                            <span>Azure OpenAI GPT-4o</span>
                            <div className="w-1 h-1 bg-border rounded-full" />
                            <span>DeepSeek-V3 Engine</span>
                        </div>
                        <Dialog>
                            <DialogTrigger asChild>
                                <Button variant="ghost" size="icon" className="h-6 w-6 text-muted-foreground/40 hover:text-foreground">
                                    <Settings2 size={14} />
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                    <DialogTitle className="flex items-center gap-2">
                                        <Terminal className="w-5 h-5" />
                                        System Configuration
                                    </DialogTitle>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="flex flex-col gap-2">
                                        <label className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Global System Prompt</label>
                                        <Textarea 
                                            value={systemPrompt} 
                                            onChange={(e) => setSystemPrompt(e.target.value)}
                                            placeholder="Define how the models should behave..."
                                            className="min-h-[150px] text-sm"
                                        />
                                        <p className="text-[10px] text-muted-foreground italic">This prompt will be sent to both models to define their persona and constraints.</p>
                                    </div>
                                </div>
                            </DialogContent>
                        </Dialog>
                    </div>
                </div>
            </div>
        </div>
    );
};
