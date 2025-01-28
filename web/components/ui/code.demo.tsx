"use client";

import { Button } from "./button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./dropdown-menu";
import { Monitor, Moon, Sun } from "lucide-react";
import { AIInputWithSuggestions } from "./ai-input-with-suggestions";
import { useTheme } from "../theme-provider";
import { useChatHistory } from "../chat-history-provider";

export function ThemeSwitcher() {
  const { theme, setTheme } = useTheme();

  return (
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button size="icon" variant="outline" aria-label="Select theme">
            {theme === "light" && <Sun size={16} strokeWidth={2} aria-hidden="true" />}
            {theme === "dark" && <Moon size={16} strokeWidth={2} aria-hidden="true" />}
            {theme === "system" && <Monitor size={16} strokeWidth={2} aria-hidden="true" />}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="min-w-32">
          <DropdownMenuItem onClick={() => setTheme("light")}>
            <Sun size={16} strokeWidth={2} className="opacity-60" aria-hidden="true" />
            <span>Light</span>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => setTheme("dark")}>
            <Moon size={16} strokeWidth={2} className="opacity-60" aria-hidden="true" />
            <span>Dark</span>
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => setTheme("system")}>
            <Monitor size={16} strokeWidth={2} className="opacity-60" aria-hidden="true" />
            <span>System</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

export function AIInputWithSuggestionsDemo() {
  const { addMessage, addResponse } = useChatHistory();

  const handleSubmit = async (text: string, action?: string) => {
    if (!text.trim()) return;

    // First add the message and get its details
    const message = addMessage(text, action);

    if (action === "Generate Image") {
      try {
        const response = await fetch('http://localhost:8000/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: text }),
        });

        if (!response.ok) {
          throw new Error('Failed to generate image');
        }

        const data = await response.json();
        addResponse(message.id, { type: "image", content: data.image });
      } catch (error) {
        addResponse(message.id, { 
          type: "text", 
          content: "Failed to generate image. Please try again." 
        });
      }
    } else {
      // Mock responses for other actions
      setTimeout(() => {
        const responses: Record<string, string> = {
          "Summary": "Here's a summary of your text: " + text,
          "Fix Spelling and Grammar": "Corrected version: " + text,
          "Make shorter": "Shortened: " + text.slice(0, text.length / 2) + "...",
        };

        addResponse(message.id, {
          type: "text",
          content: responses[action || ""] || `Received: ${text}`,
        });
      }, 500); // Small delay to simulate processing
    }
  };

  return (
    <AIInputWithSuggestions
      onSubmit={handleSubmit}
      placeholder="Try typing something..."
    />
  );
}