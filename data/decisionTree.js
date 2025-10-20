/**
 * Decision tree data structure for the LLM journalism tool advisor
 * This tree guides users through questions to recommend appropriate AI tools
 */

export const decisionTree = {
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
