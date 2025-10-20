import React, { useState, useEffect } from "react";
import "./App.css";

const App = () => {
    // --- DATA (Updated June 2025) ---
    const decisionTree = {
        start: {
            question: "What journalism task are you working on today?",
            options: [
                { text: "Research & background information", next: "research" },
                { text: "Content creation & writing", next: "content" },
                { text: "Data analysis & visualization", next: "data" },
                { text: "Editing & refining", next: "editing" },
                { text: "Source finding & management", next: "sources" },
                { text: "Multimedia content", next: "multimedia" },
            ],
        },
        research: {
            question: "What kind of research are you conducting?",
            options: [
                { text: "Quick background on a topic", next: "research_basic" },
                {
                    text: "Deep dive into a complex issue",
                    next: "research_deep",
                },
                {
                    text: "Finding recent or real-time info",
                    next: "research_recent",
                },
                {
                    text: "Analyzing specific documents",
                    next: "research_documents",
                },
            ],
        },
        research_basic: {
            question: "How specialized is your topic?",
            options: [
                {
                    text: "General knowledge topic",
                    next: "recommendation",
                    tools: [
                        {
                            name: "General purpose LLM interaction",
                            description:
                                "For broad research, brainstorming, and getting a general understanding of a topic.",
                            tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                            prompt: "Act as a research assistant. Create a comprehensive briefing document on [TOPIC]. The document should be structured with the following sections: 1. Executive Summary, 2. Historical Context, 3. Key Stakeholders and Their Positions, 4. Current State of Affairs, 5. Major Debates and Controversies. The target audience is a journalist needing to get up to speed quickly.",
                            tips: "Claude Sonnet 4 often provides a more readable, narrative-style summary. Gemini 2.5 Pro may provide a more data-dense overview. After the initial summary, ask follow-up questions to drill down into specific areas of interest.",
                        },
                    ],
                },
                {
                    text: "Niche or specialized subject",
                    next: "recommendation",
                    tools: [
                        {
                            name: "Deep research models",
                            description:
                                "For complex or specialized topics that require more careful reasoning and data processing.",
                            tools: ["ChatGPT o3", "Gemini 2.5 Pro"],
                            prompt: "You are a subject matter expert in [NICHE FIELD]. I am a journalist writing an investigative piece on [SPECIFIC NICHE TOPIC]. Explain it to me as you would a colleague. Please detail the key terminology with definitions, a timeline of major developments, the most influential figures or organizations, and three potential, non-obvious story angles worth exploring. I need you to think critically and not just summarize.",
                            tips: "ChatGPT's o3 model is a top-tier reasoning engine, making it ideal for understanding complex systems. Gemini 2.5 Pro is also excellent, especially if you have background documents to provide. Always fact-check specialized information with a human expert.",
                        },
                    ],
                },
            ],
        },
        recommendation: {
            question: "Here are your recommended tools and approaches:",
            options: [],
        },
    };

    // --- STATE ---
    const [currentStep, setCurrentStep] = useState("start");
    const [history, setHistory] = useState([]);
    const [selectedTools, setSelectedTools] = useState([]);
    const [showRecommendation, setShowRecommendation] = useState(false);

    // --- HELPER FUNCTIONS ---
    const getStepColor = (step) => {
        const colors = {
            start: "bg-indigo-600",
            research: "bg-blue-600",
            content: "bg-emerald-600",
            data: "bg-purple-600",
            editing: "bg-amber-600",
            sources: "bg-rose-600",
            multimedia: "bg-teal-600",
            default: "bg-indigo-600",
        };
        const key =
            Object.keys(colors).find((k) => step.startsWith(k)) || "default";
        return colors[key];
    };

    const getToolColor = (tool) => {
        const toolColors = {
            Claude: "bg-orange-500 text-white",
            Gemini: "bg-teal-500 text-white",
            ChatGPT: "bg-gray-800 text-white",
            Grok: "bg-blue-500 text-white",
            DeepSeek: "bg-blue-700 text-white",
            Mistral: "bg-pink-600 text-white",
            Perplexity: "bg-purple-600 text-white",
            ElevenLabs: "bg-emerald-600 text-white",
            Midjourney: "bg-indigo-700 text-white",
            Qwen: "bg-red-600 text-white",
            default: "bg-slate-500 text-white",
        };
        const key =
            Object.keys(toolColors).find((k) => tool.includes(k)) || "default";
        return toolColors[key];
    };

    // --- EVENT HANDLERS ---
    const handleOptionSelect = (option) => {
        const newHistory = [
            ...history,
            {
                step: currentStep,
                question: decisionTree[currentStep].question,
                selection: option.text,
            },
        ];
        setHistory(newHistory);

        if (option.tools) {
            setSelectedTools([...selectedTools, ...option.tools]);
        }

        if (option.next === "recommendation") {
            setShowRecommendation(true);
        } else {
            setCurrentStep(option.next);
        }
    };

    const handleRestart = () => {
        setCurrentStep("start");
        setHistory([]);
        setSelectedTools([]);
        setShowRecommendation(false);
    };

    const handleBack = () => {
        if (history.length > 0) {
            const newHistory = [...history];
            const previous = newHistory.pop();
            setHistory(newHistory);
            setCurrentStep(previous.step);
            setShowRecommendation(false);

            // Rebuild selectedTools
            const newSelectedTools = [];
            newHistory.forEach((h) => {
                const node = decisionTree[h.step];
                const option = node.options.find((o) => o.text === h.selection);
                if (option && option.tools)
                    newSelectedTools.push(...option.tools);
            });
            setSelectedTools(newSelectedTools);
        }
    };

    // --- RENDER FUNCTIONS ---
    const renderQuestionView = () => {
        const node = decisionTree[currentStep];
        return (
            <div>
                <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-white">
                    {node.question}
                </h2>
                <div className="space-y-3">
                    {node.options.map((option, index) => (
                        <button
                            key={index}
                            className="w-full text-left p-4 rounded-lg bg-white/10 hover:bg-white/20 transition-all duration-200 flex justify-between items-center text-white"
                            onClick={() => handleOptionSelect(option)}
                        >
                            <span className="text-base">{option.text}</span>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="20"
                                height="20"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="text-white flex-shrink-0 ml-2"
                            >
                                <path d="m9 18 6-6-6-6" />
                            </svg>
                        </button>
                    ))}
                </div>
            </div>
        );
    };

    const renderRecommendationView = () => {
        return (
            <div>
                <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-white">
                    Your recommended tools and approaches
                </h2>
                <div className="space-y-6">
                    {selectedTools.map((tool, index) => (
                        <div
                            key={index}
                            className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-5"
                        >
                            <h3 className="text-lg font-medium text-white flex items-center">
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    className="mr-2 text-white flex-shrink-0"
                                >
                                    <path d="M12 20s-8-4.5-8-12.5A8 8 0 0 1 12 4a8 8 0 0 1 8 8.5c0 8-8 12.5-8 12.5z" />
                                    <circle cx="12" cy="11" r="2" />
                                </svg>
                                {tool.name}
                            </h3>
                            <p className="mt-2 text-white/80">
                                {tool.description}
                            </p>

                            <div className="mt-4">
                                <h4 className="font-medium text-white">
                                    Recommended tools:
                                </h4>
                                <div className="flex flex-wrap gap-2 mt-1">
                                    {tool.tools.map((item, idx) => (
                                        <span
                                            key={idx}
                                            className={`${getToolColor(item)} px-2 py-1 rounded-full text-sm font-medium`}
                                        >
                                            {item}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className="mt-4 p-3 sm:p-4 bg-black/20 rounded border border-white/20">
                                <h4 className="font-medium text-white">
                                    Sample prompt:
                                </h4>
                                <code className="block mt-1 text-sm whitespace-pre-wrap text-white/90">
                                    {tool.prompt}
                                </code>
                            </div>

                            {tool.tips && (
                                <div className="mt-4">
                                    <h4 className="font-medium text-white">
                                        Tips:
                                    </h4>
                                    <p className="mt-1 text-white/80 text-sm">
                                        {tool.tips}
                                    </p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
                <div className="mt-6">
                    <button
                        className="px-4 py-2 bg-white/20 text-white rounded-lg hover:bg-white/30 transition-colors"
                        onClick={handleRestart}
                    >
                        Start another task
                    </button>
                </div>
            </div>
        );
    };

    // Calculate progress dynamically
    // Average depth of decision tree is approximately 3 steps
    const estimatedTotalSteps = 3;
    const progressPercentage = showRecommendation
        ? 100
        : Math.min(
              100,
              Math.round((history.length / estimatedTotalSteps) * 100),
          );

    // Get color class for current step
    const colorClass = getStepColor(currentStep);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
            <div className={`${colorClass} rounded-lg shadow-2xl max-w-4xl mx-auto overflow-hidden`}>
                {/* Header */}
                <div className="text-white p-4 sm:p-6">
                    <div className="flex justify-between items-center gap-2">
                        <h1 className="text-xl sm:text-2xl font-bold">
                            LLM journalism tool advisor
                        </h1>
                        <div className="flex space-x-2 items-center flex-shrink-0">
                            <button
                                className={`p-2 rounded-full bg-black/20 hover:bg-black/30 ${history.length === 0 ? "cursor-not-allowed opacity-50" : ""}`}
                                onClick={handleBack}
                                disabled={history.length === 0}
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="m15 18-6-6 6-6" />
                                </svg>
                            </button>
                            <button
                                className="p-2 rounded-full bg-black/20 hover:bg-black/30"
                                onClick={handleRestart}
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                                    <path d="M3 3v5h5" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <div className="mt-4 bg-black/20 rounded-full h-2">
                        <div
                            className="bg-white rounded-full h-2 transition-all duration-500 ease-in-out"
                            style={{ width: `${progressPercentage}%` }}
                        ></div>
                    </div>

                    {history.length > 0 && (
                        <div className="mt-3 flex flex-wrap items-center text-sm text-white/70">
                            {history.map((item, idx) => (
                                <React.Fragment key={idx}>
                                    <span className="truncate">
                                        {item.selection}
                                    </span>
                                    {idx < history.length - 1 && (
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            width="12"
                                            height="12"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            strokeWidth="2"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            className="mx-1 flex-shrink-0"
                                        >
                                            <path d="m9 18 6-6-6-6" />
                                        </svg>
                                    )}
                                </React.Fragment>
                            ))}
                        </div>
                    )}
                </div>

                {/* Main Content */}
                <div className="p-4 sm:p-6">
                    {showRecommendation
                        ? renderRecommendationView()
                        : renderQuestionView()}
                </div>

                {/* Footer */}
                <div className="text-white p-4 sm:p-6 border-t border-white/20">
                    <p className="text-sm text-white/70">
                        This interactive advisor helps journalists select
                        appropriate LLM tools for specific tasks. Created by{" "}
                        <a
                            href="https://twitter.com/jsamditis"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="underline hover:text-white"
                        >
                            Joe Amditis
                        </a>
                        . Updated June 2025.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default App;
