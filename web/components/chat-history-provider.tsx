"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

interface ChatMessage {
  id: string;
  text: string;
  action?: string;
  response?: {
    type: "text" | "image";
    content: string;
  };
  timestamp: number;
}

interface ChatHistoryContextType {
  messages: ChatMessage[];
  addMessage: (text: string, action?: string) => ChatMessage;
  addResponse: (messageId: string, response: { type: "text" | "image"; content: string }) => void;
  clearHistory: () => void;
}

const ChatHistoryContext = createContext<ChatHistoryContextType | undefined>(undefined);

export function ChatHistoryProvider({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Load messages from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem("chat-history");
      if (stored) {
        setMessages(JSON.parse(stored));
      }
    } catch (error) {
      console.error("Error loading chat history:", error);
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem("chat-history", JSON.stringify(messages));
    } catch (error) {
      console.error("Error saving chat history:", error);
    }
  }, [messages]);

  const addMessage = (text: string, action?: string) => {
    const newMessage: ChatMessage = {
      id: crypto.randomUUID(),
      text,
      action,
      timestamp: Date.now(),
    };
    
    setMessages(prev => [...prev, newMessage]);
    return newMessage;
  };

  const addResponse = (messageId: string, response: { type: "text" | "image"; content: string }) => {
    setMessages(prev => prev.map(msg => 
      msg.id === messageId 
        ? { ...msg, response } 
        : msg
    ));
  };

  const clearHistory = () => {
    setMessages([]);
    localStorage.removeItem("chat-history");
  };

  return (
    <ChatHistoryContext.Provider 
      value={{ 
        messages, 
        addMessage, 
        addResponse,
        clearHistory,
      }}
    >
      {children}
    </ChatHistoryContext.Provider>
  );
}

export function useChatHistory() {
  const context = useContext(ChatHistoryContext);
  if (context === undefined) {
    throw new Error("useChatHistory must be used within a ChatHistoryProvider");
  }
  return context;
}