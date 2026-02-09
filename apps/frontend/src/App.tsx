import { ChatWindow } from '@/components/ChatWindow';
import { ThemeProvider } from '@/components/theme-provider';

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="min-h-screen bg-background text-foreground transition-colors duration-300">
        <ChatWindow />
      </div>
    </ThemeProvider>
  );
}

export default App;
