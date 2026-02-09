import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion } from 'framer-motion';
import { BrainCircuit, Sparkles, User, Copy, ThumbsUp, ThumbsDown, RotateCw, Check, Clock, BarChart3 } from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { type Message } from '@/hooks/useChat';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface MessageBubbleProps {
    msg: Message;
    isUser: boolean;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ msg, isUser }) => {
    const isGPT = msg.model === 'gpt-4';
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(msg.content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
            className={cn(
                "flex w-full mb-6",
                isUser ? "justify-end" : "justify-start"
            )}
        >
            <div className={cn("flex max-w-[85%] md:max-w-[80%] gap-3", isUser ? "flex-row-reverse" : "flex-row")}>
                <Avatar className={cn(
                    "h-8 w-8 mt-1 shadow-md ring-2 ring-offset-2 ring-offset-background transition-all shrink-0",
                    isUser ? "ring-primary" : (isGPT ? "ring-blue-500" : "ring-purple-600")
                )}>
                    <AvatarFallback className={cn(
                        "font-bold text-xs flex items-center justify-center",
                        isUser ? "bg-primary text-primary-foreground" : (isGPT ? "bg-blue-600 text-white" : "bg-purple-600 text-white")
                    )}>
                        {isUser ? <User size={14} /> : (isGPT ? <Sparkles size={14} /> : <BrainCircuit size={14} />)}
                    </AvatarFallback>
                </Avatar>

                <div className="flex flex-col gap-1 items-start max-w-full min-w-0">
                    <div className={cn("flex items-center gap-2 text-[10px] uppercase tracking-wider text-muted-foreground px-1", isUser && "flex-row-reverse self-end")}>
                        <span className="font-bold">
                            {isUser ? "You" : (isGPT ? "GPT-4o" : "DeepSeek-V3")}
                        </span>
                        <span className="opacity-30">•</span>
                        <span className="opacity-50">{msg.timestamp}</span>
                        {!isUser && msg.latency && (
                            <>
                                <span className="opacity-30">•</span>
                                <span className="flex items-center gap-1 text-amber-500/80">
                                    <Clock size={10} />
                                    {msg.latency.toFixed(2)}s
                                </span>
                            </>
                        )}
                    </div>

                    <div className={cn(
                        "group relative px-4 py-3 text-sm shadow-sm transition-all hover:shadow-md overflow-hidden",
                        isUser
                            ? "bg-primary text-primary-foreground rounded-2xl rounded-tr-sm"
                            : "bg-card backdrop-blur-md border border-border/50 text-foreground rounded-2xl rounded-tl-sm"
                    )}>
                        {isUser ? (
                            <div className="whitespace-pre-wrap leading-relaxed">{msg.content}</div>
                        ) : (
                            <div className="prose prose-sm dark:prose-invert max-w-none prose-p:leading-relaxed prose-pre:p-0 prose-pre:bg-transparent">
                                <ReactMarkdown 
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        code({node, inline, className, children, ...props}: any) {
                                            const match = /language-(\w+)/.exec(className || '');
                                            return !inline && match ? (
                                                <SyntaxHighlighter
                                                    style={vscDarkPlus as any}
                                                    language={match[1]}
                                                    PreTag="div"
                                                    {...props}
                                                >
                                                    {String(children).replace(/\n$/, '')}
                                                </SyntaxHighlighter>
                                            ) : (
                                                <code className={className} {...props}>
                                                    {children}
                                                </code>
                                            );
                                        }
                                    }}
                                >
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                        )}

                        {!isUser && (
                            <div className="flex items-center gap-1 mt-3 pt-2 border-t border-border/10 opacity-0 group-hover:opacity-100 transition-opacity">
                                <Button 
                                    variant="ghost" 
                                    size="icon" 
                                    className="h-7 w-7 text-muted-foreground hover:text-foreground hover:bg-muted"
                                    onClick={handleCopy}
                                >
                                    {copied ? <Check size={12} className="text-green-500" /> : <Copy size={12} />}
                                </Button>
                                <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground hover:text-foreground hover:bg-muted">
                                    <RotateCw size={12} />
                                </Button>
                                <div className="flex-1" />
                                {msg.usage && (
                                    <div className="flex items-center gap-2 mr-2 text-[9px] text-muted-foreground/60 font-mono">
                                        <BarChart3 size={10} />
                                        {msg.usage.total_tokens} tokens
                                    </div>
                                )}
                                <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground hover:text-foreground hover:bg-muted">
                                    <ThumbsUp size={12} />
                                </Button>
                                <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground hover:text-foreground hover:bg-muted">
                                    <ThumbsDown size={12} />
                                </Button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </motion.div>
    );
};
