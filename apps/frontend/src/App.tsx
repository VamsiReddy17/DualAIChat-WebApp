import { ChatWindow } from '@/components/chat/ChatWindow';
import { ThemeProvider } from '@/components/layout/theme-provider';
import { ErrorBoundary } from '@/components/layout/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
          <ChatWindow />
        </div>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
