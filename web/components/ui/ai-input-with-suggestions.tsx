'use client';

import React from 'react';
import { TextShimmerWave } from "./text-shimmer-wave";
import { GradientTracing } from "./gradient-tracing";
import { LucideIcon } from "lucide-react";
import {
    Text,
    CheckCheck,
    ArrowDownWideNarrow,
    CornerRightDown,
    Image,
} from "lucide-react";
import { useState } from "react";
import { Textarea } from "./textarea";
import { cn } from "../../lib/utils";
import { useAutoResizeTextarea } from "../hooks/use-auto-resize-textarea";

interface ActionItem {
    text: string;
    icon: LucideIcon;
    colors: {
        icon: string;
        border: string;
        bg: string;
    };
}

interface AIInputWithSuggestionsProps {
    id?: string;
    placeholder?: string;
    minHeight?: number;
    maxHeight?: number;
    actions?: ActionItem[];
    defaultSelected?: string;
    onSubmit?: (text: string, action?: string) => void;
    className?: string;
}

interface GenerateResponse {
    image: string;
}

const DEFAULT_ACTIONS: ActionItem[] = [
    {
        text: "Summary",
        icon: Text,
        colors: {
            icon: "text-orange-600",
            border: "border-orange-500",
            bg: "bg-orange-100",
        },
    },
    {
        text: "Fix Spelling and Grammar",
        icon: CheckCheck,
        colors: {
            icon: "text-emerald-600",
            border: "border-emerald-500",
            bg: "bg-emerald-100",
        },
    },
    {
        text: "Make shorter",
        icon: ArrowDownWideNarrow,
        colors: {
            icon: "text-purple-600",
            border: "border-purple-500",
            bg: "bg-purple-100",
        },
    },
    {
        text: "Generate Image",
        icon: Image,
        colors: {
            icon: "text-blue-600",
            border: "border-blue-500",
            bg: "bg-blue-100",
        },
    },
];

export function AIInputWithSuggestions({
    id = "ai-input-with-actions",
    placeholder = "Enter your text here...",
    minHeight = 64,
    maxHeight = 200,
    actions = DEFAULT_ACTIONS,
    defaultSelected,
    onSubmit,
    className
}: AIInputWithSuggestionsProps) {
    const [inputValue, setInputValue] = useState("");
    const [selectedItem, setSelectedItem] = useState<string | null>(defaultSelected ?? null);
    const [generatedImage, setGeneratedImage] = useState<string | null>(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const { textareaRef, adjustHeight } = useAutoResizeTextarea({
        minHeight,
        maxHeight,
    });

    const toggleItem = (itemText: string) => {
        setSelectedItem((prev) => (prev === itemText ? null : itemText));
        setGeneratedImage(null);
        setError(null);
    };

    const currentItem = selectedItem
        ? actions.find((item) => item.text === selectedItem)
        : null;

    const handleImageGeneration = async (text: string) => {
        setIsGenerating(true);
        setError(null);
        setGeneratedImage(null);
        try {
            console.log('Sending request with prompt:', text);
            const response = await fetch('http://localhost:8000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: text }),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate image');
            }

            const data: GenerateResponse = await response.json();
            setGeneratedImage(data.image);
        } catch (error) {
            console.error('Error generating image:', error);
            let errorMessage = 'Failed to generate image. Please try again.';
            if (error instanceof Error) {
                errorMessage += ` (${error.message})`;
            }
            setError(errorMessage);
        } finally {
            setIsGenerating(false);
        }
    };

    const handleSubmit = async () => {
        if (inputValue.trim()) {
            if (selectedItem === "Generate Image") {
                await handleImageGeneration(inputValue);
            } else {
                onSubmit?.(inputValue, selectedItem ?? undefined);
                setInputValue("");
                setSelectedItem(null);
                adjustHeight(true);
            }
        }
    };

    return (
        <div className="relative max-w-xl mx-auto w-full">
            {/* Loading animation */}
            {isGenerating && (
                <div className="absolute left-0 right-0 -top-32 z-50 pointer-events-none">
                    <GradientTracing
                        width={800}
                        height={400}
                        path="M0,200 C200,100 600,300 800,200"
                        gradientColors={["#2EB9DF", "#2EB9DF", "#9E00FF"]}
                        animationDuration={3}
                        baseColor="#e2e8f0"
                    />
                </div>
            )}

            {/* Output section */}
            <div className="w-full space-y-4 mb-4">
                {isGenerating && (
                    <div className="text-center relative z-50">
                        <TextShimmerWave
                            className='[--base-color:#0D74CE] [--base-gradient-color:#5EB1EF]'
                            duration={1}
                            spread={1}
                            zDistance={1}
                            scaleDistance={1.1}
                            rotateYDistance={20}
                        >
                            Creating your image...
                        </TextShimmerWave>
                    </div>
                )}
                {error && (
                    <div className="text-center relative z-50">
                        <TextShimmerWave
                            className='[--base-color:#ef4444] [--base-gradient-color:#b91c1c]'
                            duration={1.5}
                            spread={1.2}
                            zDistance={1}
                            scaleDistance={1.05}
                            rotateYDistance={15}
                        >
                            {error}
                        </TextShimmerWave>
                    </div>
                )}
                {generatedImage && (
                    <div className="relative z-50">
                        <img
                            src={`data:image/png;base64,${generatedImage}`}
                            alt="Generated image"
                            className="w-full rounded-lg shadow-lg"
                        />
                    </div>
                )}
            </div>

            {/* Input section */}
            <div className={cn("relative", className)}>
                <div className="relative">
                    <div className="border border-black/10 dark:border-white/10 focus-within:border-black/20 dark:focus-within:border-white/20 rounded-2xl bg-black/[0.03] dark:bg-white/[0.03]">
                        <div className="flex flex-col">
                            <div
                                className="overflow-y-auto"
                                style={{ maxHeight: `${maxHeight - 48}px` }}
                            >
                                <Textarea
                                    ref={textareaRef}
                                    id={id}
                                    placeholder={placeholder}
                                    className={cn(
                                        "max-w-xl w-full rounded-2xl pr-10 pt-3 pb-3 placeholder:text-black/70 dark:placeholder:text-white/70 border-none focus:ring text-black dark:text-white resize-none text-wrap bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 leading-[1.2]",
                                        `min-h-[${minHeight}px]`
                                    )}
                                    value={inputValue}
                                    onChange={(e) => {
                                        setInputValue(e.target.value);
                                        adjustHeight();
                                    }}
                                    onKeyDown={(e) => {
                                        if (e.key === "Enter" && !e.shiftKey) {
                                            e.preventDefault();
                                            handleSubmit();
                                        }
                                    }}
                                    disabled={isGenerating}
                                />
                            </div>

                            <div className="h-12 bg-transparent">
                                {currentItem && (
                                    <div className="absolute left-3 bottom-3 z-50">
                                        <button
                                            type="button"
                                            onClick={handleSubmit}
                                            className={cn(
                                                "inline-flex items-center gap-1.5",
                                                "border shadow-sm rounded-md px-2 py-0.5 text-xs font-medium",
                                                "animate-fadeIn hover:bg-black/5 dark:hover:bg-white/5 transition-colors duration-200",
                                                currentItem.colors.bg,
                                                currentItem.colors.border
                                            )}
                                            disabled={isGenerating}
                                        >
                                            <currentItem.icon
                                                className={`w-3.5 h-3.5 ${currentItem.colors.icon}`}
                                            />
                                            <span className={currentItem.colors.icon}>
                                                {selectedItem}
                                            </span>
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>

                        <CornerRightDown
                            className={cn(
                                "absolute right-3 top-3 w-4 h-4 transition-all duration-200 dark:text-white",
                                inputValue
                                    ? "opacity-100 scale-100"
                                    : "opacity-30 scale-95"
                            )}
                        />
                    </div>
                </div>
                <div className="flex flex-wrap gap-1.5 mt-2 justify-start px-4">
                    {actions.filter((item) => item.text !== selectedItem).map(
                        ({ text, icon: Icon, colors }) => (
                            <button
                                type="button"
                                key={text}
                                className={cn(
                                    "px-3 py-1.5 text-xs font-medium rounded-full",
                                    "border transition-all duration-200",
                                    "border-black/10 dark:border-white/10 bg-white dark:bg-gray-900 hover:bg-black/5 dark:hover:bg-white/5",
                                    "flex-shrink-0"
                                )}
                                onClick={() => toggleItem(text)}
                                disabled={isGenerating}
                            >
                                <div className="flex items-center gap-1.5">
                                    <Icon className={cn("h-4 w-4", colors.icon)} />
                                    <span className="text-black/70 dark:text-white/70 whitespace-nowrap">
                                        {text}
                                    </span>
                                </div>
                            </button>
                        )
                    )}
                </div>
            </div>
        </div>
    );
}