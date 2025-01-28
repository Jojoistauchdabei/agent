"use client";

import { useChatHistory } from "./chat-history-provider";
import { cn } from "@/lib/utils";
import { useEffect, useRef } from "react";

function formatTime(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export function ChatHistory() {
  const { messages } = useChatHistory();
  const bottomRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground">
        <p>No messages yet</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col space-y-4 pt-20 pb-4">
      {messages.map((message, index) => (
        <div 
          key={message.id} 
          className={cn(
            "space-y-2",
            "animate-[slide-in-from-bottom_0.2s_ease-out]",
            index === messages.length - 1 && message.response && "pb-4"
          )}
        >
          {/* Message */}
          <div className="flex items-start gap-2">
            <div className="bg-primary/5 rounded-lg p-3 text-sm">
              <p className="whitespace-pre-wrap">{message.text}</p>
              {message.action && (
                <span className="text-xs text-muted-foreground mt-1 block">
                  Action: {message.action}
                </span>
              )}
              <span className="text-xs text-muted-foreground mt-1 block">
                {formatTime(message.timestamp)}
              </span>
            </div>
          </div>

          {/* Response */}
          {message.response && (
            <div className="flex items-start gap-2 pl-6">
              <div
                className={cn(
                  "bg-muted rounded-lg p-3",
                  message.response.type === "image" ? "max-w-sm" : "text-sm"
                )}
              >
                {message.response.type === "image" ? (
                  <img
                    src={`data:image/png;base64,${message.response.content}`}
                    alt="Generated"
                    className="rounded-md shadow-sm"
                  />
                ) : (
                  <p className="whitespace-pre-wrap">{message.response.content}</p>
                )}
                <span className="text-xs text-muted-foreground mt-1 block">
                  {formatTime(message.timestamp)}
                </span>
              </div>
            </div>
          )}
        </div>
      ))}
      {/* Auto-scroll anchor */}
      <div ref={bottomRef} className="h-px" />
    </div>
  );
}