import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
    Send, BrainCircuit, LayoutGrid, Sparkles, MessageSquare,
    Plus, Trash2, Settings2, Terminal, StopCircle, WifiOff,
    PanelLeftClose, PanelLeftOpen,
} from 'lucide-react';
import { DualAILogo } from '@/components/ui/DualAILogo';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { ThemeToggle } from '@/components/layout/ThemeToggle';
import { MessageBubble } from '@/components/chat/MessageBubble';
import { motion, AnimatePresence } from 'framer-motion';
import { useChat, type Message } from '@/hooks/useChat';
import { chatApi } from '@/api/chat';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";

const SUGGESTED_PROMPTS = [
    { label: "Explain quantum computing", icon: "\u{1F52C}" },
    { label: "Write a Python REST API", icon: "\u{1F40D}" },
    { label: "Compare cloud providers", icon: "\u{2601}\u{FE0F}" },
    { label: "Design a database schema", icon: "\u{1F5C4}\u{FE0F}" },
];

function safeGet(k: string) { try { return localStorage.getItem(k); } catch { return null; } }
function safeSet(k: string, v: string) { try { localStorage.setItem(k, v); } catch {} }

export const ChatWindow = () => {
    const [selectedModel, setSelectedModel] = useState<'both' | 'gpt-4' | 'deepseek'>('both');
    const chat = useChat(selectedModel);
    const { messages, setMessages, isLoading, loadingModels, sendMessage, cancelRequest, retryMessage, systemPrompt, setSystemPrompt } = chat;
    const [input, setInput] = useState('');
    const [history, setHistory] = useState<{ id: string; title: string; messages: Message[] }[]>([]);
    const [chatId, setChatId] = useState<string | null>(null);
    const [sidebar, setSidebar] = useState(true);
    const [online, setOnline] = useState(true);
    const refGPT = useRef<HTMLDivElement>(null);
    const refDS = useRef<HTMLDivElement>(null);
    const taRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => { const c = async () => setOnline(await chatApi.checkHealth()); c(); const i = setInterval(c, 30000); return () => clearInterval(i); }, []);
    useEffect(() => { const s = safeGet('chat_history'); if (s) try { setHistory(JSON.parse(s)); } catch {} }, []);
    useEffect(() => { if (history.length) safeSet('chat_history', JSON.stringify(history)); }, [history]);

    const scroll = useCallback((r: React.RefObject<HTMLDivElement | null>) => {
        if (!r.current) return;
        const el = r.current.querySelector('[data-radix-scroll-area-viewport]');
        if (el) el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
    }, []);
    useEffect(() => { scroll(refGPT); scroll(refDS); }, [messages, isLoading, scroll]);
    useEffect(() => { if (taRef.current) { taRef.current.style.height = 'auto'; taRef.current.style.height = Math.min(taRef.current.scrollHeight, 180) + 'px'; } }, [input]);

    const send = async (t: string = input) => { if (!t.trim() || isLoading) return; setInput(''); if (taRef.current) taRef.current.style.height = 'auto'; await sendMessage(t); };
    const onKey = (e: React.KeyboardEvent) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } };

    const newChat = () => {
        if (messages.length) {
            const f = messages.find(m => m.role === 'user');
            setHistory(p => [{ id: Date.now().toString(), title: f ? f.content.slice(0, 50) + (f.content.length > 50 ? '\u2026' : '') : 'New Chat', messages }, ...p]);
        }
        setMessages([]); setChatId(null);
    };

    const load = (c: { id: string; title: string; messages: Message[] }) => {
        if (messages.length && !chatId) {
            const f = messages.find(m => m.role === 'user');
            setHistory(p => [{ id: Date.now().toString(), title: f ? f.content.slice(0, 50) + '\u2026' : 'Chat', messages }, ...p]);
        }
        setMessages(c.messages); setChatId(c.id);
    };

    const lastLatency = (m: string) => { for (let i = messages.length - 1; i >= 0; i--) if (messages[i].model === m && messages[i].latency) return messages[i].latency; return null; };

    const panel = (model: 'gpt-4' | 'deepseek', label: string, sub: string, icon: React.ReactNode, color: string, bg: string, ref: React.RefObject<HTMLDivElement | null>) => {
        const lat = lastLatency(model);
        const ld = loadingModels.has(model);
        return (
            <div className={cn("flex-1 flex flex-col min-h-0 rounded-2xl border border-border/50 bg-card/50 overflow-hidden", selectedModel !== 'both' && "max-w-4xl mx-auto w-full", selectedModel === 'both' && "h-[50%] md:h-full")}>
                <div className="flex items-center justify-between px-5 py-3 border-b border-border/40">
                    <div className={cn("flex items-center gap-3", color)}>
                        <div className={cn("p-1.5 rounded-lg", bg)}>{icon}</div>
                        <div><div className="text-sm font-semibold leading-none">{label}</div><div className="text-[11px] text-muted-foreground mt-0.5">{sub}</div></div>
                    </div>
                    <div className="flex items-center gap-2">
                        {ld && <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-muted text-[11px] font-medium text-muted-foreground animate-pulse"><div className="w-1.5 h-1.5 bg-current rounded-full animate-bounce" /><div className="w-1.5 h-1.5 bg-current rounded-full animate-bounce" style={{animationDelay:'150ms'}} /><div className="w-1.5 h-1.5 bg-current rounded-full animate-bounce" style={{animationDelay:'300ms'}} /><span className="ml-1">Generating</span></div>}
                        {lat && !ld && <span className="text-[11px] font-mono text-muted-foreground bg-muted px-2 py-0.5 rounded-full">{lat.toFixed(2)}s</span>}
                    </div>
                </div>
                <ScrollArea className="flex-1 min-h-0" ref={ref}>
                    <div className="p-5 space-y-1">
                        {messages.length === 0 ? (
                            <div className="flex flex-col items-center justify-center min-h-[320px] text-center">
                                <div className={cn("w-14 h-14 rounded-2xl flex items-center justify-center mb-4", bg)}>{icon}</div>
                                <p className="text-sm font-semibold text-muted-foreground">{label}</p>
                                <p className="text-xs text-muted-foreground/80 mt-1">{sub}</p>
                            </div>
                        ) : (
                            <AnimatePresence initial={false}>
                                {messages.filter(m => m.role === 'user' || m.model === model).map(msg => (
                                    <MessageBubble key={msg.id} msg={msg} isUser={msg.role === 'user'} onRetry={msg.error ? () => retryMessage(msg.id) : undefined} />
                                ))}
                            </AnimatePresence>
                        )}
                    </div>
                </ScrollArea>
            </div>
        );
    };

    return (
        <div className="flex h-screen w-full bg-background text-foreground overflow-hidden">
            {/* Sidebar */}
            <AnimatePresence>
                {sidebar && (
                    <motion.aside initial={{width:0,opacity:0}} animate={{width:280,opacity:1}} exit={{width:0,opacity:0}} transition={{duration:0.2}} className="flex-none h-full border-r border-border/50 bg-card/30 flex flex-col overflow-hidden">
                        <div className="p-4 flex items-center gap-3 border-b border-border/40">
                            <DualAILogo size={36} />
                            <div><div className="font-bold text-sm leading-none">Dual AI Chat</div><div className="text-[11px] text-muted-foreground mt-0.5">Enterprise Edition</div></div>
                        </div>
                        <div className="p-3"><Button onClick={newChat} variant="outline" className="w-full justify-start gap-2 h-9 text-xs font-medium"><Plus className="w-3.5 h-3.5" /> New Conversation</Button></div>
                        <ScrollArea className="flex-1 px-3">
                            <div className="flex flex-col gap-1 pb-3">
                                {!history.length && <p className="text-xs text-muted-foreground/70 text-center py-8">No conversations yet</p>}
                                {history.map(c => (
                                    <div key={c.id} className={cn(
                                        "flex items-center gap-1 rounded-lg transition-colors",
                                        chatId === c.id ? "bg-muted" : "hover:bg-muted/50"
                                    )}>
                                        <button
                                            onClick={() => load(c)}
                                            className={cn(
                                                "flex-1 flex items-center gap-2 px-3 py-2 rounded-lg text-left text-xs transition-colors min-w-0",
                                                chatId === c.id ? "text-foreground" : "text-muted-foreground hover:text-foreground"
                                            )}
                                        >
                                            <MessageSquare className="w-3.5 h-3.5 shrink-0 opacity-60" />
                                            <span className="truncate">{c.title}</span>
                                        </button>
                                        <button
                                            onClick={(e) => { e.stopPropagation(); setHistory(p => p.filter(h => h.id !== c.id)); }}
                                            className="shrink-0 p-1.5 mr-1 rounded-md text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-colors"
                                            title="Delete conversation"
                                        >
                                            <Trash2 className="w-3.5 h-3.5" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </ScrollArea>
                        <div className="p-3 border-t border-border/40 flex items-center gap-2">
                            <ThemeToggle />
                            <Dialog>
                                <DialogTrigger asChild><Button variant="ghost" size="icon" className="h-9 w-9 text-muted-foreground" title="Settings"><Settings2 className="w-4 h-4" /></Button></DialogTrigger>
                                <DialogContent className="sm:max-w-md">
                                    <DialogHeader><DialogTitle className="flex items-center gap-2"><Terminal className="w-5 h-5" /> System Configuration</DialogTitle></DialogHeader>
                                    <div className="grid gap-4 py-4"><div className="flex flex-col gap-2"><label className="text-xs font-semibold text-muted-foreground">System Prompt</label><Textarea value={systemPrompt} onChange={e => setSystemPrompt(e.target.value)} placeholder="Define model behavior..." className="min-h-[140px] text-sm" /><p className="text-[11px] text-muted-foreground">Applied to both models.</p></div></div>
                                </DialogContent>
                            </Dialog>
                        </div>
                    </motion.aside>
                )}
            </AnimatePresence>

            {/* Main */}
            <div className="flex-1 flex flex-col min-w-0">
                <AnimatePresence>{!online && <motion.div initial={{height:0,opacity:0}} animate={{height:'auto',opacity:1}} exit={{height:0,opacity:0}} className="bg-destructive/10 border-b border-destructive/20 px-4 py-2 flex items-center justify-center gap-2 text-xs text-destructive font-medium"><WifiOff className="w-3.5 h-3.5" /> Backend offline</motion.div>}</AnimatePresence>

                <header className="flex-none h-14 border-b border-border/40 bg-background/80 backdrop-blur-lg flex items-center justify-between px-4 z-20">
                    <div className="flex items-center gap-2">
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setSidebar(!sidebar)}>{sidebar ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeftOpen className="w-4 h-4" />}</Button>
                        {!sidebar && <div className="flex items-center gap-2 ml-1"><DualAILogo size={28} /><span className="font-semibold text-sm">Dual AI Chat</span></div>}
                    </div>
                    <div className="flex items-center bg-muted/50 p-0.5 rounded-lg border border-border/40">
                        {([['both','Dual View',<LayoutGrid className="w-3.5 h-3.5" key="dv"/>],['gpt-4','GPT-4o',<Sparkles className="w-3.5 h-3.5 text-blue-500" key="gpt"/>],['deepseek','DeepSeek-R1',<BrainCircuit className="w-3.5 h-3.5 text-violet-500" key="ds"/>]] as const).map(([k,l,ic]) => (
                            <button key={k} onClick={() => setSelectedModel(k as any)} className={cn("flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all", selectedModel === k ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground")}>{ic} {l}</button>
                        ))}
                    </div>
                    <div className="w-20" />
                </header>

                <div className="flex-1 flex flex-col md:flex-row overflow-hidden p-3 gap-3 min-h-0">
                    {(selectedModel === 'both' || selectedModel === 'gpt-4') && panel('gpt-4', 'GPT-4o', 'Azure AI Foundry \u00b7 Fast & Versatile', <Sparkles className="w-5 h-5 text-blue-500" />, 'text-blue-600 dark:text-blue-400', 'bg-blue-500/10', refGPT)}
                    {selectedModel === 'both' && <div className="hidden md:block w-px bg-border/30 self-stretch my-6" />}
                    {(selectedModel === 'both' || selectedModel === 'deepseek') && panel('deepseek', 'DeepSeek-R1', 'Azure AI Foundry \u00b7 Reasoning', <BrainCircuit className="w-5 h-5 text-violet-500" />, 'text-violet-600 dark:text-violet-400', 'bg-violet-500/10', refDS)}
                </div>

                <div className="flex-none px-4 pb-4 pt-1">
                    <div className="max-w-4xl mx-auto flex flex-col gap-3">
                        {!messages.length && <div className="flex flex-wrap justify-center gap-2">{SUGGESTED_PROMPTS.map((p,i) => <button key={i} onClick={() => send(p.label)} disabled={isLoading} className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-border bg-card hover:bg-muted text-xs text-muted-foreground hover:text-foreground transition-all disabled:opacity-50"><span>{p.icon}</span> {p.label}</button>)}</div>}
                        <div className="flex items-end bg-card border border-border/50 rounded-2xl shadow-lg p-2 gap-2 focus-within:border-border focus-within:shadow-xl transition-all">
                            <textarea ref={taRef} placeholder={selectedModel === 'both' ? "Message both models\u2026" : `Message ${selectedModel === 'gpt-4' ? 'GPT-4o' : 'DeepSeek-R1'}\u2026`} className="flex-1 bg-transparent border-none focus:outline-none text-sm px-3 py-2.5 placeholder:text-muted-foreground/60 resize-none min-h-[44px] max-h-[180px]" value={input} onChange={e => setInput(e.target.value)} onKeyDown={onKey} disabled={isLoading} autoFocus rows={1} />
                            {isLoading
                                ? <Button size="icon" onClick={cancelRequest} className="h-9 w-9 rounded-xl bg-destructive hover:bg-destructive/90 shrink-0" title="Stop"><StopCircle className="w-4 h-4" /></Button>
                                : <Button size="icon" onClick={() => send()} disabled={!input.trim()} className={cn("h-9 w-9 rounded-xl transition-all shrink-0", input.trim() ? "bg-foreground text-background hover:bg-foreground/90" : "bg-muted text-muted-foreground")} title="Send"><Send className="w-4 h-4" /></Button>
                            }
                        </div>
                        <p className="text-[11px] text-center text-muted-foreground/70">Dual AI Chat compares GPT-4o and DeepSeek-R1 side-by-side. Shift+Enter for new line.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
