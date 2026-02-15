import React, { useState, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion } from 'framer-motion';
import { BrainCircuit, Sparkles, User, Copy, ThumbsUp, ThumbsDown, RotateCw, Check, Clock, BarChart3, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { type Message } from '@/hooks/useChat';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface Props { msg: Message; isUser: boolean; onRetry?: () => void; }

export const MessageBubble: React.FC<Props> = ({ msg, isUser, onRetry }) => {
    const isGPT = msg.model === 'gpt-4';
    const [copied, setCopied] = useState(false);
    const [feedback, setFeedback] = useState<'up'|'down'|null>(null);

    const copy = useCallback(async () => {
        try { await navigator.clipboard.writeText(msg.content); } catch {}
        setCopied(true); setTimeout(() => setCopied(false), 2000);
    }, [msg.content]);

    if (isUser) return (
        <motion.div initial={{opacity:0,y:6}} animate={{opacity:1,y:0}} transition={{duration:0.2}} className="flex justify-end mb-4">
            <div className="max-w-[80%] flex items-start gap-3 flex-row-reverse">
                <div className="w-7 h-7 rounded-full bg-foreground text-background flex items-center justify-center shrink-0 mt-0.5"><User size={14}/></div>
                <div>
                    <div className="text-[11px] text-muted-foreground text-right mb-1 pr-1">{msg.timestamp}</div>
                    <div className="bg-foreground text-background px-4 py-2.5 rounded-2xl rounded-tr-md text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</div>
                </div>
            </div>
        </motion.div>
    );

    return (
        <motion.div initial={{opacity:0,y:6}} animate={{opacity:1,y:0}} transition={{duration:0.2}} className="mb-4">
            <div className="max-w-[90%] flex items-start gap-3">
                <div className={cn("w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5", isGPT ? "bg-blue-500/15 text-blue-500" : "bg-violet-500/15 text-violet-500")}>
                    {isGPT ? <Sparkles size={14}/> : <BrainCircuit size={14}/>}
                </div>
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 text-[11px] text-muted-foreground mb-1.5">
                        <span className="font-semibold">{isGPT ? "GPT-4o" : "DeepSeek-R1"}</span>
                        <span className="opacity-50">&middot;</span>
                        <span className="opacity-80">{msg.timestamp}</span>
                        {msg.latency && <><span className="opacity-50">&middot;</span><span className="flex items-center gap-0.5 opacity-80"><Clock size={9}/> {msg.latency.toFixed(2)}s</span></>}
                    </div>
                    {msg.error && <div className="flex items-center gap-2 text-destructive text-xs mb-2 px-3 py-2 rounded-lg bg-destructive/5 border border-destructive/15"><AlertCircle size={14}/><span>Failed to generate</span>{onRetry && <button onClick={onRetry} className="ml-auto flex items-center gap-1 text-[10px] font-medium hover:underline"><RotateCw size={10}/> Retry</button>}</div>}
                    <div className="prose prose-sm dark:prose-invert max-w-none prose-p:leading-relaxed prose-p:my-1.5 prose-pre:p-0 prose-pre:bg-transparent prose-pre:my-2 prose-headings:mt-4 prose-headings:mb-2 prose-li:my-0.5 text-sm">
                        <ReactMarkdown remarkPlugins={[remarkGfm]} components={{
                            code({inline, className, children, ...props}: any) {
                                const match = /language-(\w+)/.exec(className || '');
                                const code = String(children).replace(/\n$/, '');
                                if (!inline && match) return (
                                    <div className="rounded-xl overflow-hidden border border-border/30 my-3">
                                        <div className="flex items-center justify-between bg-zinc-900 px-4 py-2 text-xs"><span className="text-zinc-400 font-mono">{match[1]}</span><CopyBtn text={code}/></div>
                                        <SyntaxHighlighter style={vscDarkPlus as any} language={match[1]} PreTag="div" customStyle={{margin:0,borderRadius:0,fontSize:'0.8rem',padding:'1rem'}} {...props}>{code}</SyntaxHighlighter>
                                    </div>
                                );
                                return <code className="bg-muted px-1.5 py-0.5 rounded text-[0.85em] font-mono" {...props}>{children}</code>;
                            }
                        }}>{msg.content}</ReactMarkdown>
                    </div>
                    {msg.content && !msg.error && (
                        <div className="flex items-center gap-0.5 mt-2 opacity-0 hover:opacity-100 focus-within:opacity-100 transition-opacity">
                            <Btn onClick={copy} title={copied?"Copied!":"Copy"}>{copied ? <Check size={13} className="text-green-500"/> : <Copy size={13}/>}</Btn>
                            {onRetry && <Btn onClick={onRetry} title="Regenerate"><RotateCw size={13}/></Btn>}
                            <div className="flex-1"/>
                            {msg.usage && <span className="text-[10px] text-muted-foreground/70 font-mono mr-1 flex items-center gap-1"><BarChart3 size={10}/> {(msg.usage as any).total_tokens} tok</span>}
                            <Btn onClick={() => setFeedback(f => f==='up'?null:'up')} title="Good" className={feedback==='up'?'text-green-500':''}><ThumbsUp size={13}/></Btn>
                            <Btn onClick={() => setFeedback(f => f==='down'?null:'down')} title="Bad" className={feedback==='down'?'text-red-500':''}><ThumbsDown size={13}/></Btn>
                        </div>
                    )}
                </div>
            </div>
        </motion.div>
    );
};

const Btn: React.FC<{onClick:()=>void;title:string;className?:string;children:React.ReactNode}> = ({onClick,title,className,children}) => (
    <button onClick={onClick} title={title} className={cn("p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors",className)}>{children}</button>
);

const CopyBtn: React.FC<{text:string}> = ({text}) => {
    const [c, setC] = useState(false);
    return <button onClick={async()=>{try{await navigator.clipboard.writeText(text)}catch{} setC(true); setTimeout(()=>setC(false),2000)}} className="flex items-center gap-1.5 text-zinc-400 hover:text-white transition-colors">{c ? <><Check size={12} className="text-green-400"/><span className="text-green-400">Copied</span></> : <><Copy size={12}/><span>Copy</span></>}</button>;
};
