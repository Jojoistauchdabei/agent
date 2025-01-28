"use client";

import { ThemeProvider } from "./theme-provider";
import { ChatHistoryProvider } from "./chat-history-provider";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <ChatHistoryProvider>
        {children}
      </ChatHistoryProvider>
    </ThemeProvider>
  );
}