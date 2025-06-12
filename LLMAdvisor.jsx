import React, { useState, useEffect } from 'react';
import { ChevronRight, RefreshCw, X, Award, Sparkles, BookOpen, BrainCircuit, Bot, Scale, Link as LinkIcon } from 'lucide-react';
import VanillaTilt from 'vanilla-tilt';

const LLMAdvisor = () => {
    // --- DATA (Updated June 2025) ---
    const decisionTree = {
        start: { question: "What journalism task are you working on today?", options: [ { text: "Research & background information", next: "research" }, { text: "Content creation & writing", next: "content" }, { text: "Data analysis & visualization", next: "data" }, { text: "Editing & refining", next: "editing" }, { text: "Source finding & management", next: "sources" }, { text: "Multimedia content", next: "multimedia" } ] },
        research: { question: "What kind of research are you conducting?", options: [ { text: "Quick background on a topic", next: "research_basic" }, { text: "Deep dive into a complex issue", next: "research_deep" }, { text: "Finding recent or real-time info", next: "research_recent" }, { text: "Analyzing specific documents", next: "research_documents" } ] },
        research_basic: { question: "How specialized is your topic?", options: [ { text: "General knowledge topic", next: "recommendation", tools: [{ name: "General purpose LLM interaction", description: "For broad research, brainstorming, and getting a general understanding of a topic.", tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"], prompt: "Act as a research assistant. Create a comprehensive briefing document on [TOPIC]. The document should be structured with the following sections: 1. Executive Summary, 2. Historical Context, 3. Key Stakeholders and Their Positions, 4. Current State of Affairs, 5. Major Debates and Controversies. The target audience is a journalist needing to get up to speed quickly.", tips: "Claude Sonnet 4 often provides a more readable, narrative-style summary. Gemini 2.5 Pro may provide a more data-dense overview. After the initial summary, ask follow-up questions to drill down into specific areas of interest." }] }, { text: "Niche or specialized subject", next: "recommendation", tools: [{ name: "Deep research models", description: "For complex or specialized topics that require more careful reasoning and data processing.", tools: ["ChatGPT o3", "Gemini 2.5 Pro"], prompt: "You are a subject matter expert in [NICHE FIELD]. I am a journalist writing an investigative piece on [SPECIFIC NICHE TOPIC]. Explain it to me as you would a colleague. Please detail the key terminology with definitions, a timeline of major developments, the most influential figures or organizations, and three potential, non-obvious story angles worth exploring. I need you to think critically and not just summarize.", tips: "ChatGPT's o3 model is a top-tier reasoning engine, making it ideal for understanding complex systems. Gemini 2.5 Pro is also excellent, especially if you have background documents to provide. Always fact-check specialized information with a human expert." }] } ] },
        research_deep: { question: "Do you have specific documents to analyze?", options: [ { text: "Yes, I have a large collection of documents", next: "recommendation", tools: [{ name: "Large context document analysis", description: "Use models with large context windows to process and synthesize entire document collections.", tools: ["Gemini 2.5 Pro", "Claude Sonnet 4"], prompt: "Act as an investigative data analyst. I have uploaded a collection of [NUMBER] documents related to [TOPIC]. Your task is to: 1. Cross-reference all documents to create a master timeline of events. 2. Identify any conflicting information or inconsistencies between the documents. 3. Extract all names of people and corporations mentioned. 4. Provide a summary of the most critical finding supported by evidence from the provided files, citing which document the evidence comes from.", tips: "This is the ideal use case for Gemini 2.5 Pro due to its massive 1M+ token context window. For smaller collections (under ~150k tokens), Claude Sonnet 4 also performs exceptionally well and may provide a more narrative summary." }] }, { text: "No, I'm starting from scratch", next: "recommendation", tools: [{ name: "Investigative research tools", description: "Use specialized research modes to find and synthesize information from the web.", tools: ["ChatGPT o3/o4 (Deep Research)", "Grok 3 (DeepSearch)"], prompt: "I am beginning an investigative report on [COMPLEX TOPIC]. I need a comprehensive research plan. Please provide: 1. A list of 10 keywords and search phrases I should use. 2. A list of potential source types (e.g., academic journals, government reports, court filings, NGOs). 3. Three potential narrative arcs for the story. 4. A list of key ethical considerations for this topic.", tips: "In ChatGPT, use the o3 or o4 model and explicitly trigger the 'Deep Research' feature which is more thorough. In Grok 3, use the 'DeepSearch' function for a similar, exhaustive search focused on current events. This is for lead generation—all findings must be independently verified." }] } ] },
        research_recent: { question: "How time-sensitive is your information need?", options: [ { text: "Breaking news & real-time social media", next: "recommendation", tools: [{ name: "Real-time news monitoring", description: "Use LLMs integrated with real-time data streams for up-to-the-minute information.", tools: ["Grok 3"], prompt: "Monitor X/Twitter for the topic [EVENT/TOPIC]. Provide a summary of developments over the last 30 minutes. Identify the 5 most influential accounts (by engagement) discussing this topic. What is the prevailing sentiment? Is there any emerging misinformation?", tips: "Grok 3's direct X/Twitter integration is its killer feature. Use it to find eyewitnesses or see how a narrative is forming online in real-time. Treat everything as a lead, not a fact. Always verify." }] }, { text: "Recent news (last few days/weeks)", next: "recommendation", tools: [{ name: "Web-connected LLMs", description: "Use search-enabled LLMs to find information from the recent past.", tools: ["ChatGPT o4", "Perplexity"], prompt: "Provide a chronological summary of news coverage about [TOPIC] from the last 7 days. For each key development, cite the primary news source with a URL. Distinguish between official statements and pundit commentary. Conclude with a list of unanswered questions based on the current reporting.", tips: "These tools are essentially intelligent search engines. The key is to review the *original sources* they cite. Never take the summary at face value without clicking through to read the context from the source article." }] } ] },
        research_documents: { question: "What is your main goal with these documents?", options: [ { text: "Summarize and find key insights", next: "recommendation", tools: [{ name: "Document analysis & summarization", description: "Analyze text-based documents (PDFs, reports) to extract key information.", tools: ["Gemini 2.5 Pro", "Claude Sonnet 4"], prompt: "I have uploaded a [DOCUMENT TYPE]. Act as a policy analyst. Provide the following: 1. A one-paragraph executive summary. 2. A bulleted list of the top 5 most impactful conclusions. 3. A table extracting all statistics, data points, and their corresponding sources mentioned in the document. 4. A list of any jargon or acronyms and their definitions.", tips: "Use Gemini 2.5 Pro if you have a very large document or a whole folder of them. Use Claude Sonnet 4 if your priority is a well-written, nuanced summary from a single, moderately-sized document." }] }, { text: "Analyze and visualize data from files", next: "recommendation", tools: [{ name: "Data file analysis", description: "Analyze structured data from files like CSVs or spreadsheets to find trends and create charts.", tools: ["ChatGPT o3", "Gemini 2.5 Pro", "DeepSeek R1"], prompt: "I have uploaded a CSV file containing [DATASET DESCRIPTION]. Act as a data journalist. Analyze this data to find the three most newsworthy insights. For each insight, explain why it is significant, generate a corresponding data visualization (e.g., bar chart, line graph), and provide the Python code you used for the analysis.", tips: "Use Gemini 2.5 Pro to perform the analysis and create the chart directly. Use ChatGPT o3 for its top-tier reasoning if the analysis requires complex logical steps. For pure analytical power on a budget, DeepSeek R1 is excellent." }] } ] },
        content: { question: "What type of content are you creating?", options: [ { text: "Article drafting or writing assistance", next: "content_writing" }, { text: "Headline and social media copy", next: "content_social" }, { text: "Interview question preparation", next: "content_interview" } ] },
        content_writing: { question: "What stage of writing are you in?", options: [ { text: "Brainstorming and outlining", next: "recommendation", tools: [{ name: "Story angle explorer", description: "Use an LLM to brainstorm different angles and structures for a story.", tools: ["Claude Sonnet 4", "ChatGPT o4"], prompt: "I'm developing a story about [TOPIC]. My target audience is [AUDIENCE DESCRIPTION]. Generate three distinct narrative structures for this story: 1. Inverted Pyramid (for a hard news approach). 2. Narrative Arc (for a feature story). 3. Explainer (for a deep dive). For each, provide a brief outline and a compelling lede.", tips: "Claude's conversational and creative style often leads to more unique and nuanced story angles. It's like having a very creative editor to bounce ideas off of. Use this for the initial 'what if' stage of reporting." }] }, { text: "Writing a first draft", next: "recommendation", tools: [{ name: "Long-form writing assistant", description: "Generate a first draft of an article based on your notes and research.", tools: ["Claude Sonnet 4"], prompt: "You are a feature writer for [PUBLICATION-STYLE, e.g., The New Yorker]. Using only the provided notes, quotes, and data below, write a compelling 800-word narrative article. Weave the quotes in naturally and use the data to support the story. Do not add any information not present in the notes. NOTES: [PASTE YOUR DETAILED NOTES, QUOTES, and DATA]", tips: "Claude Sonnet 4 is the industry leader for this task. The output quality is directly proportional to the detail and quality of your input notes. This is a tool to assemble your reporting, not to do the reporting for you. The draft will still require rigorous fact-checking and editing." }] } ] },
        content_social: { question: "What kind of copy do you need?", options: [ { text: "Headlines for an article", next: "recommendation", tools: [{ name: "Headline generator", description: "Generate multiple headline options for an article, optimized for SEO or engagement.", tools: ["Claude Sonnet 4", "ChatGPT o4"], prompt: "I've written an article about [TOPIC]. The main takeaway is [MAIN TAKEAWAY]. The target keyword is '[KEYWORD]'. Generate 10 headline options: 5 optimized for Google search results (under 60 characters, including the keyword), and 5 optimized for high engagement on social media (e.g., posing a question, using a compelling stat). Ensure all headlines are accurate and not clickbait.", tips: "For best results, paste the full text of your article into the LLM first and ask it to summarize the key points. Use that summary to inform your headline generation prompt for more accurate and compelling options." }] }, { text: "A cross-platform social media package", next: "recommendation", tools: [{ name: "Social media package creator", description: "Create tailored posts for different social media platforms from a single article.", tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"], prompt: "Here is my article: [PASTE ARTICLE TEXT]. Create a promotional social media package. The package should include: 1. Two posts for X/Twitter (one with a key quote, one with a surprising stat), including relevant hashtags and tagging [@RELEVANT_ACCOUNTS]. 2. One professional post for LinkedIn, aimed at industry experts. 3. One engaging post for Facebook that asks a question to drive comments.", tips: "After generating the text, ask the model to suggest a specific type of visual for each post (e.g., 'For the Facebook post, an infographic showing the key statistic would work well.')." }] } ] },
        content_interview: { question: "Who are you interviewing?", options: [ { text: "An expert or public figure", next: "recommendation", tools: [{ name: "Expert interview preparation", description: "Generate insightful questions for subject matter experts.", tools: ["ChatGPT o3/o4", "Claude Sonnet 4"], prompt: "I am interviewing [PERSON], an expert in [FIELD]. I have pasted their biography and three of their recent articles below. First, summarize their main arguments and known positions on [TOPIC]. Second, based on this research, generate 15 critical, open-ended questions that go beyond simple clarification and challenge them to elaborate on their views. Avoid questions they have likely been asked before. RESEARCH MATERIAL: [PASTE BIO AND ARTICLES]", tips: "Pro-tip workflow: Use a web-connected model like ChatGPT o4 to compile a dossier on your subject. Then, paste that complete dossier into a reasoning model like ChatGPT o3 or Claude Sonnet 4 to craft truly unique and effective questions." }] }, { text: "A person with a personal story (human interest)", next: "recommendation", tools: [{ name: "Human interest interview guide", description: "Generate sensitive and narrative-focused questions for personal stories.", tools: ["Claude Sonnet 4"], prompt: "You are a trauma-informed journalist. I am interviewing someone about their personal experience with [SENSITIVE TOPIC]. My goal is to empower them to tell their story in their own words. Generate 12 questions that are empathetic, open-ended, and non-judgmental. Order the questions to build rapport first before moving to more difficult topics. Conclude with questions about their hopes for the future.", tips: "Claude's strength in understanding emotional nuance makes it the only choice for this kind of sensitive work. Its ability to generate gentle, respectful questions is unmatched. Read the questions carefully and use your own judgment during the actual interview." }] } ] },
        data: { question: "What are you trying to do with data?", options: [ { text: "Analyze a dataset to find stories", next: "data_analysis" }, { text: "Generate code for data work", next: "data_coding" }, { text: "Extract structured data from documents", next: "data_extraction" } ] },
        data_analysis: { question: "What is your main goal?", options: [ { text: "Find trends and create visualizations", next: "recommendation", tools: [{ name: "Advanced data analysis & visualization", description: "Analyze structured data files to find trends and create charts directly within the chat interface.", tools: ["Gemini 2.5 Pro"], prompt: "I've uploaded a dataset about [TOPIC]. Act as a data journalist. Your task is to: 1. Perform an exploratory data analysis to understand the dataset. 2. Identify the three most statistically significant and newsworthy insights. 3. For each insight, explain it in a single paragraph. 4. Generate a clean, well-labeled data visualization for each of the three insights.", tips: "Gemini 2.5 Pro is the best tool for this because it has powerful, built-in data analysis and visualization capabilities (sometimes called 'code interpreter' functionality). You can upload a file and have it work directly on the data without writing code yourself." }] }, { text: "Perform complex analysis on a budget", next: "recommendation", tools: [{ name: "Cost-effective complex reasoning", description: "Use highly efficient models for complex mathematical or logical analysis.", tools: ["DeepSeek R1"], prompt: "I have a complex dataset on [TOPIC]. I need to perform a [SPECIFIC STATISTICAL ANALYSIS, e.g., multiple regression analysis] to determine the relationship between [VARIABLE 1] and [VARIABLE 2]. Provide the results, an interpretation of their statistical significance, and any caveats about the methodology.", tips: "When your newsroom is facing budget constraints but needs to perform serious data analysis, DeepSeek R1 offers analytical power comparable to top-tier models at a fraction of the API cost. It's a specialist tool for when you need math, not prose." }] } ] },
        data_coding: { question: "What kind of coding help do you need?", options: [ { text: "Writing scripts for analysis or scraping", next: "recommendation", tools: [{ name: "Coding assistant for journalists", description: "Generate and debug code for data analysis, visualization, or web scraping.", tools: ["Claude Sonnet 4"], prompt: "You are an expert Python developer specializing in data journalism. Write a well-commented Python script that uses the 'pandas' and 'matplotlib' libraries. The script should: 1. Load the dataset from 'data.csv'. 2. Clean the data by removing rows with missing values in the '[COLUMN_NAME]' column. 3. Calculate the average of '[COLUMN_A]' grouped by '[COLUMN_B]'. 4. Create and save a bar chart of the result, titled 'Average [A] by [B]'.", tips: "Claude Sonnet 4 is now widely considered the best AI for coding assistance. It excels at generating clean, functional, and well-explained code. You can also paste your own broken code and ask it to find the error and fix it." }] }, { text: "Quick code checks and simple scripts", next: "recommendation", tools: [{ name: "Fast and lightweight code generation", description: "For when you need a quick script or a code snippet without waiting.", tools: ["Mistral Small 3", "Qwen 2.5"], prompt: "Write a javascript bookmarklet that allows me to select text on a page and automatically perform a Google search for that selected text in a new tab.", tips: "These smaller, open-source models are incredibly fast. For simple, everyday coding tasks, they can provide an answer almost instantly. They can also be run locally on your own machine using tools like Ollama for ultimate privacy and speed." }] } ] },
        data_extraction: { question: "What is your source format?", options: [ { text: "PDFs, scanned documents, or reports", next: "recommendation", tools: [{ name: "Document data extractor", description: "Extract structured data (like names, dates, numbers) from unstructured text documents.", tools: ["Gemini 2.5 Pro", "Claude Sonnet 4"], prompt: "I have uploaded a 100-page PDF report. Scan the entire document and extract every instance of a person's name, their stated job title, and the organization they work for. Your output must be a valid CSV-formatted table with three columns: 'Name', 'Title', 'Organization'. Do not include any other text or explanation.", tips: "For this kind of structured data extraction from large files, Gemini 2.5 Pro is the most reliable tool due to its large context window. For smaller files, Claude is also excellent. The key to success is being extremely specific about the desired output format, as in the prompt above." }] }, { text: "Web pages", next: "recommendation", tools: [{ name: "Web scraping code generator", description: "Generate a script to extract information from websites.", tools: ["Claude Sonnet 4"], prompt: "I need to extract the headline, author, and publication date for every article listed on this news hub page: [URL]. Please provide a complete, runnable Python script using the 'requests' and 'Beautiful Soup' libraries. The script should save the extracted data into a CSV file named 'articles.csv'. Include comments explaining each part of the script.", tips: "Claude Sonnet 4 is the top choice for generating clean, well-commented code. Important: Always check a website's 'robots.txt' file and terms of service before scraping to ensure you are complying with their policies. Be a good internet citizen." }] } ] },
        editing: { question: "What kind of editing assistance do you need?", options: [ { text: "Copy editing (grammar and style)", next: "recommendation", tools: [{ name: "AI copy editor", description: "Review text for grammar, spelling, punctuation, and adherence to a style guide.", tools: ["Claude Sonnet 4"], prompt: "Act as the lead copy editor for the Associated Press. Review the following text for any grammatical errors, spelling mistakes, and punctuation issues. Ensure every part of it strictly follows the latest AP style guide. For each correction you make, briefly explain the rule that justifies the change. TEXT: [PASTE TEXT]", tips: "Claude Sonnet 4 is the most nuanced and 'human-like' AI editor. For even better results, you can create a custom project where you upload your newsroom's specific style guide, and it will learn to edit according to your rules, not just general ones." }] }, { text: "Structural and developmental editing", next: "recommendation", tools: [{ name: "AI developmental editor", description: "Get feedback on the structure, flow, and narrative of your draft.", tools: ["Claude Sonnet 4"], prompt: "You are a seasoned developmental editor known for giving candid, constructive feedback. I am providing my draft article below. I want you to read it and provide feedback in the following format: 1. Overall Thesis: Is it clear and well-supported? 2. Structure and Flow: Where does the narrative drag or lose focus? 3. Lede/Introduction: Does it successfully hook the reader? 4. Strongest & Weakest Sections: Identify them and explain why. 5. A Final Provocative Question: What is the one thing I'm not thinking about that would make this piece better? DRAFT: [PASTE DRAFT]", tips: "Don't just accept the feedback. Argue with it. Ask 'why do you think that?' to get deeper insights. Using the model as a Socratic partner is more valuable than just using it as a proofreader. Claude is the best tool for this high-level, nuanced feedback." }] } ] },
        sources: { question: "What do you need help with regarding sources?", options: [ { text: "Finding new sources", next: "recommendation", tools: [{ name: "Expert source finder", description: "Identify potential experts, organizations, and individuals to interview for a story.", tools: ["ChatGPT o4", "Perplexity"], prompt: "I am writing an article on [TOPIC] and need to find diverse, expert sources. Please identify five potential experts, ensuring they represent a range of perspectives (e.g., academic, industry, activist). For each expert, provide: their name, current affiliation, a brief summary of their known stance on the topic, and a link to their professional profile or contact page.", tips: "These tools are connected to the web, making them ideal for discovery. Be specific in your prompt to find sources with different viewpoints to avoid creating a one-sided story. Always independently vet the credentials of any source suggested by an AI." }] }, { text: "Organizing and preparing for interviews", next: "recommendation", tools: [{ name: "Interview preparation assistant", description: "Create a dossier on an interview subject and generate questions.", tools: ["ChatGPT o4", "Claude Sonnet 4"], prompt: "I am interviewing [PERSON] tomorrow about their new book, '[BOOK TITLE]'. First, act as a research assistant and compile a dossier on this person including their career history, major achievements, past controversies, and common themes in their work. Second, act as an expert journalist and, based on that dossier, generate 10 insightful questions that have not been asked in other recent interviews.", tips: "This two-step process is key. Use a web-connected tool like ChatGPT to do the background research. Then, feed that research into a more conversationally nuanced tool like Claude Sonnet 4 to craft truly unique and effective questions." }] } ] },
        multimedia: { question: "What are you creating?", options: [ { text: "Audio (podcasts, voiceovers)", next: "recommendation", tools: [{ name: "AI voice and audio tools", description: "Generate high-quality voiceovers or get assistance with podcast production.", tools: ["ElevenLabs", "Claude Sonnet 4"], prompt: "For ElevenLabs: 'Convert the following article text into a realistic, professional audio voiceover using a standard American English male voice. Ensure the pacing is appropriate for a news report. TEXT: [TEXT]'. For Claude: 'I am planning a 15-minute podcast episode on [TOPIC]. Provide a three-act structure for the episode, suggest a compelling cold open, and write a script for the intro and outro segments.'", tips: "Use specialized tools like ElevenLabs when the final audio quality is the top priority. Use general-purpose models like Claude for the conceptual and writing stages of production, like scripting and planning." }] }, { text: "Images (conceptual illustrations)", next: "recommendation", tools: [{ name: "AI image generation", description: "Create conceptual images or illustrations for articles when photography isn't an option.", tools: ["Midjourney", "DALL-E 3 (in ChatGPT)"], prompt: "Generate a conceptual, photorealistic image for a feature story about the ethical dilemmas of artificial intelligence in healthcare. The image should be somber and thought-provoking, not dystopian. It should feature a doctor looking at a glowing, abstract neural network, with a concerned but determined expression. The composition should be asymmetrical. Avoid using any text or cliché robot imagery.", tips: "Midjourney often produces more artistic and higher-quality images but has a steeper learning curve. DALL-E 3 is easier to use as it's integrated into ChatGPT. Being extremely descriptive and providing stylistic and emotional direction is key to getting a good result. Always disclose AI-generated images according to your publication's policy." }] } ] },
        recommendation: { question: "Here are your recommended tools and approaches:", options: [] }
    };
    const toolComparisonData = {
        "Claude Sonnet 4": { strengths: ["Most 'human-like' for writing and editing", "Best-in-class coding support", "Excellent for conversational interviews"], weaknesses: ["Lower usage limits on paid tier compared to some", "No voice chat feature"], bestFor: ["Long-form writing", "Editing drafts", "Coding assistance"], pricing: "Free tier available; $20/month for paid features" },
        "Gemini 2.5 Pro": { strengths: ["Largest context window (1M+ tokens)", "Excellent for processing huge documents", "Strong data analysis and visualization"], weaknesses: ["Less conversational and can feel impersonal", "Pricing is usage-based, can be costly"], bestFor: ["Investigative research", "Analyzing large datasets", "Summarizing document collections"], pricing: "Usage-based (e.g., $1.25/million input tokens)" },
        "ChatGPT o4": { strengths: ["Excellent 'Deep Research' feature", "Good memory across conversations", "Best voice chat functionality"], weaknesses: ["Can sometimes reference past conversations inappropriately", "Smaller context window than Gemini"], bestFor: ["General research", "Fact-checking", "Meeting preparation"], pricing: "$20/month for paid tier" },
        "ChatGPT o3": { strengths: ["Top-tier logical and complex reasoning", "Excellent for multi-step analytical tasks", "Shows its 'chain of thought' effectively"], weaknesses: ["Not designed for creative or conversational tasks", "Can be slower due to complex processing"], bestFor: ["Investigative deduction", "Analyzing complex arguments", "Fact-checking logical chains"], pricing: "Included with paid tier" },
        "Grok 3": { strengths: ["Direct, real-time X/Twitter integration", "Excellent for breaking news and social media trends", "DeepSearch for current events"], weaknesses: ["Less polished for general writing tasks", "Outputs can be more variable"], bestFor: ["Real-time news monitoring", "Social media analysis", "Finding sources during breaking news"], pricing: "Free tier available" },
        "DeepSeek R1": { strengths: ["Extremely cost-efficient for complex tasks", "Excellent for mathematical and logical reasoning", "Strong analytical power"], weaknesses: ["Newer platform with a less established ecosystem", "Not a general-purpose writing tool"], bestFor: ["Budget-conscious data analysis", "Complex investigations", "Fact-checking logical claims"], pricing: "Up to 30x more cost-efficient than competitors" },
        "Mistral Small 3": { strengths: ["Extremely fast and lightweight", "Can run on modest local hardware", "Fully open-source"], weaknesses: ["Less powerful than larger models for deep analysis", "Requires more technical setup to run locally"], bestFor: ["Quick fact-checks", "Real-time applications", "Privacy-focused local workflows"], pricing: "Open-source (free)" }
    };
    const caseStudiesData = [ /* ... case study data remains the same ... */ ];
    const bestPracticesData = { /* ... best practices data remains the same ... */ };
    const modelInfoData = { /* ... model info data remains the same ... */ };

  // --- STATE and DOM Refs---
  const [currentStep, setCurrentStep] = useState('start');
  const [history, setHistory] = useState([]);
  const [selectedTools, setSelectedTools] = useState([]);
  const [compareTools, setCompareTools] = useState([]);
  const [showRecommendation, setShowRecommendation] = useState(false);
  const [showRandomWorkflow, setShowRandomWorkflow] = useState(false);
  const [randomWorkflow, setRandomWorkflow] = useState(null);

  const [showComparisonModal, setShowComparisonModal] = useState(false);
  const [showCaseStudiesModal, setShowCaseStudiesModal] = useState(false);
  const [showBestPracticesModal, setShowBestPracticesModal] = useState(false);
  const [showModelInfoModal, setShowModelInfoModal] = useState(false);
  const [highlightModel, setHighlightModel] = useState(null);

  const [progress, setProgress] = useState(0);
  const [fadeIn, setFadeIn] = useState(true);

  // --- Helper Functions ---
  const getStepColor = (step) => {
    const colors = {
        start: 'bg-indigo-600', research: 'bg-blue-600', content: 'bg-emerald-600',
        data: 'bg-purple-600', editing: 'bg-amber-600', sources: 'bg-rose-600',
        multimedia: 'bg-teal-600', default: 'bg-indigo-600'
    };
    const key = Object.keys(colors).find(k => step.startsWith(k)) || 'default';
    return colors[key];
  };

  const getToolColor = (tool) => {
    const toolColors = {
        'Claude': 'bg-orange-500 text-white',
        'Gemini': 'bg-teal-500 text-white',
        'ChatGPT': 'bg-gray-800 text-white',
        'Grok': 'bg-blue-500 text-white',
        'DeepSeek': 'bg-blue-700 text-white',
        'Mistral': 'bg-pink-600 text-white',
        'Perplexity': 'bg-purple-600 text-white',
        'ElevenLabs': 'bg-emerald-600 text-white',
        'Midjourney': 'bg-indigo-700 text-white',
        'Qwen': 'bg-red-600 text-white',
        'default': 'bg-slate-500 text-white'
    };
    const key = Object.keys(toolColors).find(k => tool.includes(k)) || 'default';
    return toolColors[key];
  };

  // --- Event Handlers ---
  const handleSelect = (option) => {
    setFadeIn(false);
    setTimeout(() => {
      setHistory([...history, { step: currentStep, question: decisionTree[currentStep].question, selection: option.text }]);
      if (option.tools) {
        setSelectedTools([...selectedTools, ...option.tools]);
      }
      if (option.next === "recommendation") {
        setShowRecommendation(true);
      }
      const estimatedTotalSteps = 4;
      setProgress(Math.min(100, Math.round(((history.length + 1) / estimatedTotalSteps) * 100)));
      setCurrentStep(option.next);
      setFadeIn(true);
    }, 150);
  };

  const handleRestart = () => {
    setFadeIn(false);
    setTimeout(() => {
      setCurrentStep('start');
      setHistory([]);
      setSelectedTools([]);
      setShowRecommendation(false);
      setShowRandomWorkflow(false);
      setProgress(0);
      setFadeIn(true);
    }, 150);
  };

  const handleBack = () => {
    if (history.length > 0) {
      setFadeIn(false);
      setTimeout(() => {
        const newHistory = [...history];
        const previousStep = newHistory.pop();
        setHistory(newHistory);
        setCurrentStep(previousStep.step);
        setShowRecommendation(false);
        setShowRandomWorkflow(false);
        const estimatedTotalSteps = 4;
        setProgress(Math.min(100, Math.round((newHistory.length / estimatedTotalSteps) * 100)));
        setFadeIn(true);
      }, 150);
    }
  };

  // --- JSX Render ---
  return (
    <div className={`main-container flex flex-col rounded-lg shadow-2xl overflow-hidden w-full max-w-4xl mx-auto ${getStepColor(currentStep)}`}>
      <div className="text-white p-4 sm:p-6 transition-colors duration-300">
        <div className="flex justify-between items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold">LLM journalism tool advisor</h1>
            <div className="flex space-x-2 items-center flex-shrink-0">
                <button onClick={handleBack} disabled={history.length === 0} className="p-2 rounded-full bg-black/20 hover:bg-black/30 disabled:opacity-50 disabled:cursor-not-allowed" aria-label="Go back">
                    <ChevronRight className="w-5 h-5 transform -rotate-180" />
                </button>
                <button onClick={handleRestart} className="p-2 rounded-full bg-black/20 hover:bg-black/30" aria-label="Restart">
                    <RefreshCw className="w-5 h-5" />
                </button>
            </div>
        </div>
        <div className="mt-4 bg-black/20 rounded-full h-2">
          <div className="bg-white rounded-full h-2 transition-all duration-500 ease-in-out" style={{ width: `${progress}%` }}></div>
        </div>
      </div>

      <div className="p-4 sm:p-6 bg-gray-50 dark:bg-gray-800 flex-grow">
        {showRecommendation ? (
          <div style={{ opacity: fadeIn ? 1 : 0, transition: 'opacity 150ms' }}>
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2 flex items-center">
                <Award className="w-6 h-6 mr-2 text-indigo-600" />
                Your Recommended Tools
              </h2>
              <p className="text-gray-600 dark:text-gray-300">Based on your selections, here are the best AI tools for your task:</p>```python

            </div>

            <div className="space-y-6">
              {selectedTools.map((toolCategory, categoryIndex) => (
                <div key={categoryIndex} className="bg-white dark:bg-gray-700 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-600">
                  <div className="mb-4">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 flex items-center">
                      <Sparkles className="w-5 h-5 mr-2 text-yellow-500" />
                      {toolCategory.name}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300">{toolCategory.description}</p>
                  </div>

                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center">
                      <Bot className="w-4 h-4 mr-2 text-blue-500" />
                      Recommended Tools:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {toolCategory.tools.map((tool, toolIndex) => (
                        <span
                          key={toolIndex}
                          className={`px-3 py-1 rounded-full text-sm font-medium ${getToolColor(tool)}`}
                        >
                          {tool}
                        </span>
                      ))}
                    </div>
                  </div>

                  {toolCategory.prompt && (
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center">
                        <BookOpen className="w-4 h-4 mr-2 text-green-500" />
                        Suggested Prompt:
                      </h4>
                      <div className="bg-gray-100 dark:bg-gray-600 p-3 rounded-lg">
                        <p className="text-sm text-gray-700 dark:text-gray-200 font-mono">{toolCategory.prompt}</p>
                      </div>
                    </div>
                  )}

                  {toolCategory.tips && (
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white mb-2 flex items-center">
                        <BrainCircuit className="w-4 h-4 mr-2 text-purple-500" />
                        Pro Tips:
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-300">{toolCategory.tips}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="mt-8 flex flex-wrap gap-3">
              <button
                onClick={() => setShowComparisonModal(true)}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Scale className="w-4 h-4 mr-2" />
                Compare Tools
              </button>
              <button
                onClick={() => setShowCaseStudiesModal(true)}
                className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <BookOpen className="w-4 h-4 mr-2" />
                Case Studies
              </button>
              <button
                onClick={() => setShowBestPracticesModal(true)}
                className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                <Award className="w-4 h-4 mr-2" />
                Best Practices
              </button>
            </div>
          </div>
        ) : showRandomWorkflow ? (
          <div style={{ opacity: fadeIn ? 1 : 0, transition: 'opacity 150ms' }}>
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Random Workflow Generator</h2>
              <p className="text-gray-600 dark:text-gray-300 mb-6">Get a random journalism workflow to try something new!</p>
              <button
                onClick={() => {
                  const workflows = Object.values(decisionTree).filter(step => step.tools).flatMap(step => step.tools);
                  const randomTool = workflows[Math.floor(Math.random() * workflows.length)];
                  setRandomWorkflow(randomTool);
                }}
                className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors mb-6"
              >
                Generate Random Workflow
              </button>
              {randomWorkflow && (
                <div className="bg-white dark:bg-gray-700 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-600">
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{randomWorkflow.name}</h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">{randomWorkflow.description}</p>
                  <div className="text-left">
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Try this prompt:</h4>
                    <div className="bg-gray-100 dark:bg-gray-600 p-3 rounded-lg">
                      <p className="text-sm text-gray-700 dark:text-gray-200 font-mono">{randomWorkflow.prompt}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div style={{ opacity: fadeIn ? 1 : 0, transition: 'opacity 150ms' }}>
            <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-gray-900 dark:text-white">{decisionTree[currentStep].question}</h2>
            <div className="space-y-3">
              {decisionTree[currentStep].options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleSelect(option)}
                  className="w-full text-left p-4 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-indigo-50 dark:hover:bg-gray-600 hover:border-indigo-300 dark:hover:border-indigo-500 transition-all duration-200 flex justify-between items-center transform active:scale-95"
                >
                  <span className="text-base text-gray-900 dark:text-white">{option.text}</span>
                  <ChevronRight className="w-5 h-5 text-indigo-500" />
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Modals */}
        {showComparisonModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Tool Comparison</h2>
                <button
                  onClick={() => setShowComparisonModal(false)}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="p-6">
                <div className="grid gap-4">
                  {Object.entries(toolComparisonData).map(([tool, data]) => (
                    <div key={tool} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{tool}</h3>
                      <div className="grid md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <h4 className="font-medium text-green-600 dark:text-green-400 mb-1">Strengths</h4>
                          <ul className="text-gray-600 dark:text-gray-300">
                            {data.strengths.map((strength, idx) => (
                              <li key={idx}>• {strength}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-medium text-red-600 dark:text-red-400 mb-1">Weaknesses</h4>
                          <ul className="text-gray-600 dark:text-gray-300">
                            {data.weaknesses.map((weakness, idx) => (
                              <li key={idx}>• {weakness}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-medium text-blue-600 dark:text-blue-400 mb-1">Best For</h4>
                          <ul className="text-gray-600 dark:text-gray-300">
                            {data.bestFor.map((use, idx) => (
                              <li key={idx}>• {use}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                      <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                        <strong>Pricing:</strong> {data.pricing}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {showCaseStudiesModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Case Studies</h2>
                <button
                  onClick={() => setShowCaseStudiesModal(false)}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="p-6">
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  Real-world examples of how newsrooms are using AI tools effectively.
                </p>
                <div className="space-y-4">
                  {caseStudiesData.map((study, index) => (
                    <div key={index} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{study.title}</h3>
                      <p className="text-gray-600 dark:text-gray-300 mb-2">{study.description}</p>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        <strong>Tools used:</strong> {study.tools.join(', ')}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {showBestPracticesModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Best Practices</h2>
                <button
                  onClick={() => setShowBestPracticesModal(false)}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="p-6">
                <div className="space-y-6">
                  {Object.entries(bestPracticesData).map(([category, practices]) => (
                    <div key={category}>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 capitalize">
                        {category.replace('_', ' ')}
                      </h3>
                      <ul className="space-y-2">
                        {practices.map((practice, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-green-500 mr-2 mt-1">•</span>
                            <span className="text-gray-600 dark:text-gray-300">{practice}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {showModelInfoModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Model Information</h2>
                <button
                  onClick={() => setShowModelInfoModal(false)}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="p-6">
                <div className="grid gap-4">
                  {Object.entries(modelInfoData).map(([model, info]) => (
                    <div key={model} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{model}</h3>
                      <p className="text-gray-600 dark:text-gray-300 mb-2">{info.description}</p>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        <div><strong>Context Window:</strong> {info.contextWindow}</div>
                        <div><strong>Pricing:</strong> {info.pricing}</div>
                        <div><strong>Best Use Cases:</strong> {info.bestUseCases.join(', ')}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="flex flex-wrap justify-center gap-2 text-sm">
          <button
            onClick={() => setShowRandomWorkflow(!showRandomWorkflow)}
            className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            🎲 Random Workflow
          </button>
          <button
            onClick={() => setShowModelInfoModal(true)}
            className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
          >
            <LinkIcon className="w-3 h-3 mr-1" />
            Model Info
          </button>
        </div>
      </div>
    </div>
  );
};

export default LLMAdvisor;