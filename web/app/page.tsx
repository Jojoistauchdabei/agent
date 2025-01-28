"use client";

import { AIInputWithSuggestionsDemo, ThemeSwitcher } from "../components/ui/code.demo";
import { ChatHistory } from "../components/chat-history";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Theme switcher fixed at top */}
      <div className="fixed top-4 right-4 z-50">
        <ThemeSwitcher />
      </div>

      {/* Main content area with chat history and input */}
      <div className="flex-grow flex flex-col">
        {/* Chat history with scrolling */}
        <div className="flex-grow overflow-hidden">
          <div className="h-full overflow-y-auto p-4">
            <div className="max-w-xl mx-auto">
              <ChatHistory />
            </div>
          </div>
        </div>
        
        {/* Input fixed at bottom */}
        <div className="w-full border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="max-w-xl mx-auto p-4">
            <AIInputWithSuggestionsDemo />
          </div>
        </div>
      </div>
    </div>
  );
}