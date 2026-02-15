import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Props { children: React.ReactNode; }
interface State { hasError: boolean; error: Error | null; }

export class ErrorBoundary extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false, error: null };
    }
    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }
    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error("ErrorBoundary caught:", error, errorInfo);
    }
    render() {
        if (this.state.hasError) {
            return (
                <div className="flex flex-col items-center justify-center min-h-screen bg-background text-foreground p-8">
                    <div className="flex flex-col items-center gap-4 max-w-md text-center">
                        <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center">
                            <AlertTriangle className="w-8 h-8 text-destructive" />
                        </div>
                        <h2 className="text-xl font-bold">Something went wrong</h2>
                        <p className="text-sm text-muted-foreground">{this.state.error?.message || "An unexpected error occurred."}</p>
                        <Button onClick={() => { this.setState({ hasError: false, error: null }); window.location.reload(); }} className="gap-2">
                            <RefreshCw className="w-4 h-4" /> Reload App
                        </Button>
                    </div>
                </div>
            );
        }
        return this.props.children;
    }
}
