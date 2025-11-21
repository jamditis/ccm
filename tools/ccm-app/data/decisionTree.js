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
    // Content Creation Branch
    content: {
        question: "What type of content are you creating?",
        options: [
            { text: "Article or news story", next: "content_article" },
            { text: "Headlines and social media posts", next: "content_social" },
            { text: "Long-form feature or investigation", next: "content_longform" },
            { text: "Scripts for video or audio", next: "content_scripts" },
        ],
    },
    content_article: {
        question: "What's your main challenge?",
        options: [
            {
                text: "Starting from scratch / writer's block",
                next: "recommendation",
                tools: [
                    {
                        name: "Creative writing assistants",
                        description: "For drafting initial content, overcoming writer's block, and generating story structures.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "I'm writing a [NEWS/FEATURE/OPINION] article about [TOPIC]. Help me create an outline with: 1. A compelling lede that hooks readers, 2. Three main sections with key points to cover, 3. Potential quotes or perspectives to seek out, 4. A strong conclusion. My audience is [DESCRIBE AUDIENCE] and the tone should be [TONE].",
                        tips: "Use these tools to generate ideas and structure, but always add your own reporting, verification, and voice. Claude excels at nuanced storytelling, while ChatGPT can provide multiple angle options quickly.",
                    },
                ],
            },
            {
                text: "Improving draft quality",
                next: "recommendation",
                tools: [
                    {
                        name: "Editorial enhancement tools",
                        description: "For refining existing drafts, improving clarity, and strengthening arguments.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Review this article draft and provide: 1. Suggestions to strengthen weak paragraphs, 2. Areas where I need more evidence or examples, 3. Transitions that could be smoother, 4. Sentences that could be more concise. Here's my draft: [PASTE DRAFT]",
                        tips: "These models can spot logical gaps and clarity issues. However, maintain your journalistic voice and editorial judgment. Always fact-check any suggestions before incorporating them.",
                    },
                ],
            },
        ],
    },
    content_social: {
        question: "What platform are you targeting?",
        options: [
            {
                text: "Twitter/X or threads",
                next: "recommendation",
                tools: [
                    {
                        name: "Concise content generators",
                        description: "For creating punchy, engaging short-form content within character limits.",
                        tools: ["ChatGPT 4o", "Claude Sonnet 4"],
                        prompt: "Create 5 different Twitter/X post variations for this article about [TOPIC]. Requirements: 1. Each under 280 characters, 2. Include a hook that drives clicks, 3. One version should pose a question, 4. One should highlight a surprising fact, 5. One should create urgency. Article summary: [SUMMARY]",
                        tips: "Generate multiple options and A/B test them. ChatGPT 4o is faster for batch generation. Always review for accuracy and tone before posting.",
                    },
                ],
            },
            {
                text: "LinkedIn or professional networks",
                next: "recommendation",
                tools: [
                    {
                        name: "Professional content tools",
                        description: "For creating authoritative, professional-toned content with appropriate depth.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Create a LinkedIn post about [ARTICLE/TOPIC] that: 1. Opens with a thought-provoking question or insight, 2. Provides 3-4 key takeaways in a professional tone, 3. Includes relevant context for a professional audience, 4. Ends with a call-to-action for discussion. Keep it 200-300 words.",
                        tips: "Claude excels at professional tone. Add relevant hashtags manually. Consider including your own expert commentary to add unique value.",
                    },
                ],
            },
        ],
    },
    content_longform: {
        question: "Where do you need the most help?",
        options: [
            {
                text: "Structuring complex narratives",
                next: "recommendation",
                tools: [
                    {
                        name: "Narrative structure assistants",
                        description: "For organizing complex stories with multiple threads and timelines.",
                        tools: ["Claude Sonnet 4", "ChatGPT o3"],
                        prompt: "I'm writing a long-form investigation about [TOPIC]. I have these elements: [LIST MAIN POINTS, CHARACTERS, TIMELINE EVENTS]. Help me: 1. Suggest a narrative structure (chronological, thematic, or hybrid), 2. Identify the most compelling entry point, 3. Suggest where to reveal key information for maximum impact, 4. Propose section breaks and transitions.",
                        tips: "ChatGPT o3 excels at complex logical structuring. Use it for the framework, but your reporting and prose should remain authentically yours. Consider multiple structural approaches.",
                    },
                ],
            },
            {
                text: "Maintaining consistency and flow",
                next: "recommendation",
                tools: [
                    {
                        name: "Editorial coherence tools",
                        description: "For ensuring consistency in long documents and smooth narrative flow.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Review this long-form piece for: 1. Consistency in character descriptions and details, 2. Timeline accuracy and clarity, 3. Repetitive phrasing or ideas, 4. Pacing issues (sections that drag or rush), 5. Thematic thread strength throughout. Document: [PASTE TEXT OR SECTIONS]",
                        tips: "For documents over 10,000 words, review in sections. Claude's large context window makes it excellent for maintaining continuity across lengthy pieces.",
                    },
                ],
            },
        ],
    },
    content_scripts: {
        question: "What format do you need?",
        options: [
            {
                text: "Video script or documentary",
                next: "recommendation",
                tools: [
                    {
                        name: "Visual storytelling assistants",
                        description: "For creating scripts optimized for visual media with scene descriptions.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "Create a [LENGTH] video script about [TOPIC] formatted as: 1. SCENE with visual description, 2. NARRATION with exact words to say, 3. B-ROLL suggestions, 4. INTERVIEW sound bite placements. Target audience: [AUDIENCE]. Key message: [MESSAGE]. Include timing estimates.",
                        tips: "Claude provides more nuanced scene descriptions. Always time your scripts by reading aloud. Include notes for editors on pacing and tone.",
                    },
                ],
            },
            {
                text: "Podcast or audio story",
                next: "recommendation",
                tools: [
                    {
                        name: "Audio narrative tools",
                        description: "For creating engaging audio scripts with sound-driven storytelling.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Write a podcast script for [TOPIC] that includes: 1. A cold open hook (30 seconds), 2. Introduction with context, 3. Main narrative with clear act breaks, 4. Places for interview clips or sound effects, 5. A memorable conclusion. Length: [DURATION]. Style: [CONVERSATIONAL/NARRATIVE/INTERVIEW].",
                        tips: "Write for the ear, not the eye. Claude excels at conversational tone. Read your script aloud multiple times. Mark places for natural pauses and emphasis.",
                    },
                ],
            },
        ],
    },
    // Data Analysis Branch
    data: {
        question: "What type of data work do you need help with?",
        options: [
            { text: "Understanding datasets", next: "data_understanding" },
            { text: "Finding patterns or insights", next: "data_analysis" },
            { text: "Creating visualizations", next: "data_visualization" },
            { text: "Explaining findings to readers", next: "data_storytelling" },
        ],
    },
    data_understanding: {
        question: "What's your data format?",
        options: [
            {
                text: "Spreadsheets or CSV files",
                next: "recommendation",
                tools: [
                    {
                        name: "Data interpretation assistants",
                        description: "For understanding datasets, identifying key columns, and spotting initial patterns.",
                        tools: ["ChatGPT 4o with Code Interpreter", "Claude Sonnet 4"],
                        prompt: "I have a dataset with these columns: [LIST COLUMNS]. Help me: 1. Identify which columns are most newsworthy, 2. Suggest what questions this data could answer, 3. Recommend initial analysis approaches, 4. Flag potential data quality issues to check. Sample rows: [PASTE 5-10 SAMPLE ROWS]",
                        tips: "ChatGPT's Code Interpreter can directly analyze uploaded CSV files. Start with summary statistics before diving into complex analysis. Always verify unusual findings in the original data.",
                    },
                ],
            },
            {
                text: "Public records or government data",
                next: "recommendation",
                tools: [
                    {
                        name: "Structured data specialists",
                        description: "For navigating complex public datasets and understanding bureaucratic data structures.",
                        tools: ["ChatGPT o3", "Gemini 2.5 Pro"],
                        prompt: "I'm analyzing [TYPE OF PUBLIC RECORDS] data. Help me: 1. Understand what each field means in plain language, 2. Identify which fields are most likely to contain newsworthy information, 3. Suggest how to cross-reference with other datasets, 4. Explain any common data quality issues with this type of record.",
                        tips: "ChatGPT o3's reasoning capabilities help decode complex government schemas. Always verify your understanding against documentation or expert sources.",
                    },
                ],
            },
        ],
    },
    data_analysis: {
        question: "What kind of analysis do you need?",
        options: [
            {
                text: "Statistical analysis or trends",
                next: "recommendation",
                tools: [
                    {
                        name: "Statistical analysis guides",
                        description: "For guidance on appropriate statistical methods and trend analysis.",
                        tools: ["ChatGPT 4o with Code Interpreter", "Claude Sonnet 4"],
                        prompt: "I want to analyze [DESCRIBE DATA] to investigate [HYPOTHESIS/QUESTION]. Help me: 1. Choose the right statistical method, 2. Identify what calculations to perform, 3. Explain how to interpret results, 4. Warn about common statistical pitfalls. I have [SAMPLE SIZE] records spanning [TIME PERIOD].",
                        tips: "Code Interpreter can perform actual calculations. Always consider confounding variables and correlation vs. causation. Consult with a data expert for complex statistical claims.",
                    },
                ],
            },
            {
                text: "Comparing groups or detecting outliers",
                next: "recommendation",
                tools: [
                    {
                        name: "Comparative analysis tools",
                        description: "For identifying anomalies, outliers, and meaningful comparisons in data.",
                        tools: ["ChatGPT 4o", "Gemini 2.5 Pro"],
                        prompt: "Help me compare [GROUP A] vs [GROUP B] in this dataset. I want to: 1. Identify statistically significant differences, 2. Find notable outliers worth investigating, 3. Determine if differences are meaningful beyond just statistical significance, 4. Suggest follow-up questions for reporting. Context: [DESCRIBE DATA]",
                        tips: "Statistical significance doesn't always equal newsworthiness. Look for substantive differences that matter to people. Always investigate outliers—they often lead to the best stories.",
                    },
                ],
            },
        ],
    },
    data_visualization: {
        question: "What kind of visualization do you need?",
        options: [
            {
                text: "Charts and graphs",
                next: "recommendation",
                tools: [
                    {
                        name: "Visualization planning assistants",
                        description: "For choosing appropriate chart types and visualization approaches.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "I want to visualize [DATA DESCRIPTION]. My key finding is [MAIN POINT]. Help me: 1. Choose the best chart type (bar, line, scatter, etc.) and explain why, 2. Suggest what to put on each axis, 3. Recommend how to highlight the key insight, 4. Identify potential misleading visual elements to avoid.",
                        tips: "Claude excels at visualization design thinking. Remember: simplicity is key. One chart should communicate one clear message. Consider your audience's data literacy level.",
                    },
                ],
            },
            {
                text: "Maps or geographic analysis",
                next: "recommendation",
                tools: [
                    {
                        name: "Geographic visualization guides",
                        description: "For creating effective maps and geographic data presentations.",
                        tools: ["ChatGPT 4o", "Claude Sonnet 4"],
                        prompt: "I have geographic data showing [DESCRIBE DATA] across [LOCATIONS]. Help me: 1. Decide between choropleth, point, or heat map, 2. Choose appropriate geographic boundaries, 3. Select a color scheme that's accessible and not misleading, 4. Determine if a map is the best choice vs. other formats.",
                        tips: "Maps are intuitive but can be misleading if not done carefully. Normalize for population when appropriate. Consider whether a simple chart might communicate your point more clearly.",
                    },
                ],
            },
        ],
    },
    data_storytelling: {
        question: "Who is your audience?",
        options: [
            {
                text: "General public / non-technical readers",
                next: "recommendation",
                tools: [
                    {
                        name: "Data storytelling for general audiences",
                        description: "For translating complex data findings into accessible narratives.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "I found that [DATA FINDING]. Help me explain this to a general audience: 1. Create an analogy that makes the scale/significance clear, 2. Write a plain-language explanation avoiding jargon, 3. Suggest a human story that illustrates the data, 4. Anticipate and address questions readers will have.",
                        tips: "Claude excels at accessible explanations. Always include the 'so what'—why should readers care? Use concrete examples and comparisons to familiar things.",
                    },
                ],
            },
            {
                text: "Specialized / professional audience",
                next: "recommendation",
                tools: [
                    {
                        name: "Technical data communication",
                        description: "For presenting data findings to audiences comfortable with data and statistics.",
                        tools: ["ChatGPT o3", "Gemini 2.5 Pro"],
                        prompt: "Present these findings to a [SPECIALIZED AUDIENCE]: [DATA FINDINGS]. Help me: 1. Structure the findings with appropriate technical detail, 2. Include methodology notes and limitations, 3. Suggest additional analyses this audience will expect, 4. Frame findings in context of field standards.",
                        tips: "Don't oversimplify for expert audiences—they'll lose trust. Include methodological transparency. ChatGPT o3 handles complex technical communication well.",
                    },
                ],
            },
        ],
    },
    // Editing Branch
    editing: {
        question: "What stage of editing are you in?",
        options: [
            { text: "Structural / big-picture issues", next: "editing_structure" },
            { text: "Clarity and readability", next: "editing_clarity" },
            { text: "Grammar and style", next: "editing_grammar" },
            { text: "Fact-checking and accuracy", next: "editing_factcheck" },
        ],
    },
    editing_structure: {
        question: "What's your main concern?",
        options: [
            {
                text: "Story organization and flow",
                next: "recommendation",
                tools: [
                    {
                        name: "Structural editing assistants",
                        description: "For evaluating overall story structure, flow, and logical progression.",
                        tools: ["Claude Sonnet 4", "ChatGPT o3"],
                        prompt: "Review this draft's structure: [PASTE DRAFT]. Provide: 1. Assessment of whether the lede buries important information, 2. Suggestions for reordering sections to improve flow, 3. Identification of tangents or digressions, 4. Recommendations for what to cut or expand.",
                        tips: "ChatGPT o3's reasoning helps identify logical issues. Be open to major restructuring if needed. The best structure serves the reader's understanding, not your writing process.",
                    },
                ],
            },
            {
                text: "Balancing perspectives and fairness",
                next: "recommendation",
                tools: [
                    {
                        name: "Editorial balance checkers",
                        description: "For identifying bias, ensuring fair representation of perspectives, and strengthening objectivity.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Analyze this article for balance: [PASTE DRAFT]. Help me: 1. Identify any perspectives that are missing or underrepresented, 2. Flag language that might reveal bias, 3. Suggest questions I should ask opposing viewpoints, 4. Ensure facts are clearly separated from opinion.",
                        tips: "Claude is particularly good at identifying subtle bias. However, balance doesn't always mean false equivalency—weigh evidence appropriately. Consider having diverse colleagues review as well.",
                    },
                ],
            },
        ],
    },
    editing_clarity: {
        question: "What clarity issue are you addressing?",
        options: [
            {
                text: "Simplifying complex topics",
                next: "recommendation",
                tools: [
                    {
                        name: "Clarity enhancement tools",
                        description: "For making complex topics more accessible without oversimplifying.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "This section explains [COMPLEX TOPIC]: [PASTE TEXT]. Help me: 1. Identify jargon that needs defining or replacing, 2. Suggest analogies to clarify difficult concepts, 3. Break down long, complex sentences, 4. Add transitions that guide readers through the logic.",
                        tips: "Claude excels at maintaining nuance while improving clarity. Test your revised text on someone unfamiliar with the topic. If they understand it, you've succeeded.",
                    },
                ],
            },
            {
                text: "Tightening wordy prose",
                next: "recommendation",
                tools: [
                    {
                        name: "Conciseness tools",
                        description: "For eliminating wordiness and strengthening prose through concision.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Make this more concise without losing important information: [PASTE TEXT]. Show me: 1. Which phrases are redundant or unnecessary, 2. Where passive voice could become active, 3. Nominalizations that could be verbs, 4. A revised version with explanation of cuts made.",
                        tips: "Aim to cut 10-20% without losing meaning. Every word should earn its place. Gemini is particularly efficient at identifying redundancies.",
                    },
                ],
            },
        ],
    },
    editing_grammar: {
        question: "What level of refinement do you need?",
        options: [
            {
                text: "Grammar and punctuation errors",
                next: "recommendation",
                tools: [
                    {
                        name: "Grammar and mechanics checkers",
                        description: "For catching grammatical errors, punctuation issues, and style inconsistencies.",
                        tools: ["ChatGPT 4o", "Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Proofread this text for grammar, punctuation, and style errors: [PASTE TEXT]. Flag: 1. Subject-verb disagreement, 2. Pronoun reference issues, 3. Punctuation errors, 4. Inconsistent tense or voice, 5. Style guide violations [SPECIFY YOUR STYLE GUIDE: AP, Chicago, etc.]",
                        tips: "All major LLMs handle basic grammar well. Don't rely solely on AI—traditional proofreading tools and human editors catch different issues. Read aloud to catch rhythm problems.",
                    },
                ],
            },
            {
                text: "Style consistency and tone",
                next: "recommendation",
                tools: [
                    {
                        name: "Style and tone refinement",
                        description: "For ensuring consistent voice, appropriate tone, and adherence to publication style.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Review this for style consistency: [PASTE TEXT]. I'm writing for [PUBLICATION] with a [FORMAL/CONVERSATIONAL/etc.] tone. Check: 1. Tone consistency throughout, 2. Voice (active vs. passive), 3. Formality level, 4. Word choice appropriateness for audience.",
                        tips: "Claude is excellent at understanding subtle tone shifts. Create a style sheet for recurring issues. Consistency builds reader trust.",
                    },
                ],
            },
        ],
    },
    editing_factcheck: {
        question: "What type of verification do you need?",
        options: [
            {
                text: "Checking claims and statements",
                next: "recommendation",
                tools: [
                    {
                        name: "Claim verification assistants",
                        description: "For identifying claims that need verification and suggesting verification approaches.",
                        tools: ["Perplexity", "ChatGPT 4o with browsing"],
                        prompt: "Identify all factual claims in this text that need verification: [PASTE TEXT]. For each claim: 1. Mark whether it's presented as fact vs. opinion, 2. Indicate if it requires a source citation, 3. Suggest what type of source would verify it, 4. Flag claims that seem questionable or surprising.",
                        tips: "Perplexity includes citations, making it useful for quick verification. However, ALWAYS verify important claims with authoritative primary sources. Never trust AI alone for fact-checking.",
                    },
                ],
            },
            {
                text: "Verifying numbers and statistics",
                next: "recommendation",
                tools: [
                    {
                        name: "Numerical accuracy checkers",
                        description: "For double-checking calculations, conversions, and statistical claims.",
                        tools: ["ChatGPT 4o with Code Interpreter", "Claude Sonnet 4"],
                        prompt: "Check these numbers and calculations: [PASTE TEXT WITH NUMBERS]. Verify: 1. Mathematical accuracy of any calculations, 2. Unit conversions, 3. Percentage calculations, 4. Whether statistics are being interpreted correctly, 5. If numbers are internally consistent.",
                        tips: "Use Code Interpreter for complex calculations. Check units carefully—metric vs. imperial, millions vs. billions. Verify numbers against original sources, not secondary reports.",
                    },
                ],
            },
        ],
    },
    // Sources Branch
    sources: {
        question: "What do you need help with regarding sources?",
        options: [
            { text: "Finding potential sources", next: "sources_finding" },
            { text: "Preparing interview questions", next: "sources_interviews" },
            { text: "Organizing source information", next: "sources_organization" },
            { text: "Evaluating source credibility", next: "sources_credibility" },
        ],
    },
    sources_finding: {
        question: "What type of sources are you looking for?",
        options: [
            {
                text: "Expert sources or academics",
                next: "recommendation",
                tools: [
                    {
                        name: "Expert identification tools",
                        description: "For finding relevant experts, academics, and authoritative sources.",
                        tools: ["Perplexity", "Gemini 2.5 Pro"],
                        prompt: "I'm reporting on [TOPIC]. Help me identify: 1. Leading researchers or experts in this field, 2. Which institutions or organizations have relevant expertise, 3. Academic papers or publications I should review, 4. Potential sources who represent different perspectives on this issue.",
                        tips: "Perplexity provides citations you can follow. Cross-reference with university directories and Google Scholar. Look for people who've published recently on the topic.",
                    },
                ],
            },
            {
                text: "People affected by an issue",
                next: "recommendation",
                tools: [
                    {
                        name: "Human source identification aids",
                        description: "For finding individuals with relevant personal experiences and perspectives.",
                        tools: ["ChatGPT 4o", "Claude Sonnet 4"],
                        prompt: "I'm covering [ISSUE/EVENT]. Help me: 1. Identify which types of people are most affected, 2. Suggest where to find these sources (communities, organizations, forums), 3. Recommend sensitive approaches for initial contact, 4. List questions to screen potential sources for relevance.",
                        tips: "AI can suggest source types and venues, but actual source finding requires human outreach. Be especially careful with vulnerable populations. Build trust before asking for interviews.",
                    },
                ],
            },
        ],
    },
    sources_interviews: {
        question: "What's your interview challenge?",
        options: [
            {
                text: "Preparing questions",
                next: "recommendation",
                tools: [
                    {
                        name: "Interview preparation assistants",
                        description: "For developing effective interview questions and strategies.",
                        tools: ["Claude Sonnet 4", "ChatGPT o3"],
                        prompt: "I'm interviewing [SOURCE DESCRIPTION] about [TOPIC]. Help me prepare: 1. 10 essential questions starting with basics and building to harder questions, 2. Follow-up questions for likely answers, 3. Questions to verify key facts, 4. Ways to ask about sensitive topics tactfully.",
                        tips: "ChatGPT o3 is good at anticipating response paths. Prepare more questions than you'll need. Listen carefully and ask follow-ups beyond your prepared list—the best material often comes from unexpected directions.",
                    },
                ],
            },
            {
                text: "Handling difficult interviews",
                next: "recommendation",
                tools: [
                    {
                        name: "Difficult interview strategists",
                        description: "For approaching hostile, evasive, or challenging interview subjects.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "I need to interview [DESCRIPTION] who may be [HOSTILE/EVASIVE/DEFENSIVE] about [TOPIC]. Help me: 1. Phrase questions to minimize defensiveness, 2. Prepare for likely evasions or pivots, 3. Develop follow-ups for non-answers, 4. Balance persistence with professionalism.",
                        tips: "Claude provides nuanced communication strategies. Document everything. Be firm but fair. If someone stonewalls, that's often newsworthy itself. Consider email interviews for evasive sources—written records are valuable.",
                    },
                ],
            },
        ],
    },
    sources_organization: {
        question: "How do you need to organize your sources?",
        options: [
            {
                text: "Tracking multiple sources and quotes",
                next: "recommendation",
                tools: [
                    {
                        name: "Source management strategists",
                        description: "For creating systems to track sources, quotes, and attribution throughout reporting.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "I'm juggling [NUMBER] sources for this story on [TOPIC]. Help me create: 1. A system for tracking who said what, 2. How to categorize sources by perspective/expertise, 3. A format for organizing quotes by theme, 4. A checklist for ensuring proper attribution.",
                        tips: "Create your tracking system early, before interviews pile up. Use consistent formatting. Claude can suggest organizational schemes, but you'll need dedicated tools (spreadsheets, Airtable, or specialized journalism software) for actual tracking.",
                    },
                ],
            },
            {
                text: "Synthesizing conflicting accounts",
                next: "recommendation",
                tools: [
                    {
                        name: "Conflict synthesis assistants",
                        description: "For analyzing and presenting conflicting source accounts fairly.",
                        tools: ["Claude Sonnet 4", "ChatGPT o3"],
                        prompt: "I have conflicting accounts: Source A says [ACCOUNT A], Source B says [ACCOUNT B], Source C says [ACCOUNT C]. Help me: 1. Identify the specific points of disagreement, 2. Determine what's corroborated vs. disputed, 3. Suggest how to present this fairly, 4. Identify what additional reporting could resolve conflicts.",
                        tips: "ChatGPT o3's reasoning helps map disagreements. Don't artificially flatten genuine disputes. Report the disagreement itself when appropriate. Corroborate with documents when possible.",
                    },
                ],
            },
        ],
    },
    sources_credibility: {
        question: "What credibility concerns do you have?",
        options: [
            {
                text: "Evaluating source reliability",
                next: "recommendation",
                tools: [
                    {
                        name: "Source evaluation guides",
                        description: "For assessing source credibility, potential biases, and reliability.",
                        tools: ["Perplexity", "Claude Sonnet 4"],
                        prompt: "Help me evaluate this source: [SOURCE DESCRIPTION AND CLAIMS]. Research: 1. Their background and expertise, 2. Potential conflicts of interest or biases, 3. Track record of accuracy, 4. How other credible sources view them, 5. Red flags in their claims.",
                        tips: "Perplexity can surface background information with citations. Trust but verify—even well-credentialed sources can be wrong. Look for multiple independent sources confirming important claims.",
                    },
                ],
            },
            {
                text: "Detecting potential misinformation",
                next: "recommendation",
                tools: [
                    {
                        name: "Misinformation detection aids",
                        description: "For identifying red flags and verifying suspicious claims.",
                        tools: ["Perplexity", "ChatGPT 4o with browsing"],
                        prompt: "This claim seems questionable: [CLAIM]. Help me: 1. Identify red flags or warning signs, 2. Find authoritative sources addressing this claim, 3. Check if it matches known misinformation patterns, 4. Suggest verification approaches, 5. Determine what evidence would confirm or debunk it.",
                        tips: "Check claim databases like Snopes, PolitiFact, and fact-checking networks. Reverse image search for photos. Be especially skeptical of emotionally charged claims and statistics without sources.",
                    },
                ],
            },
        ],
    },
    // Multimedia Branch
    multimedia: {
        question: "What type of multimedia are you working on?",
        options: [
            { text: "Photography or images", next: "multimedia_photo" },
            { text: "Video content", next: "multimedia_video" },
            { text: "Audio or podcasts", next: "multimedia_audio" },
            { text: "Interactive or visual storytelling", next: "multimedia_interactive" },
        ],
    },
    multimedia_photo: {
        question: "What's your photography challenge?",
        options: [
            {
                text: "Planning photo shoots",
                next: "recommendation",
                tools: [
                    {
                        name: "Photo shoot planning assistants",
                        description: "For planning visual story elements and photo shoot logistics.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "I'm planning a photo shoot for a story about [TOPIC]. Help me: 1. Identify key visual moments or scenes to capture, 2. Suggest shot list priorities, 3. Plan for different lighting/weather scenarios, 4. Consider ethical issues (permissions, privacy, dignity), 5. Think about visual diversity.",
                        tips: "Great visual storytelling starts with planning. Scout locations when possible. Consider how photos will work with text. Always prioritize subject dignity and consent.",
                    },
                ],
            },
            {
                text: "Writing captions and photo stories",
                next: "recommendation",
                tools: [
                    {
                        name: "Caption and photo story writers",
                        description: "For crafting effective captions and structuring visual narratives.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "Write a caption for this photo: [DESCRIBE IMAGE]. Include: 1. Essential context (who, what, where, when), 2. Why this moment matters to the story, 3. Proper identifications and attributions, 4. Keep it concise but informative. Story context: [BRIEF STORY SUMMARY].",
                        tips: "Claude excels at concise, informative captions. Captions should add context, not just describe what's visible. Always verify names and identifications. Follow AP style for photo credits.",
                    },
                ],
            },
        ],
    },
    multimedia_video: {
        question: "What aspect of video production?",
        options: [
            {
                text: "Planning and storyboarding",
                next: "recommendation",
                tools: [
                    {
                        name: "Video planning and storyboard assistants",
                        description: "For planning video structure, shots, and visual sequences.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "Help me plan a [LENGTH] video about [TOPIC]. Create: 1. A shot list with specific scenes and angles, 2. Storyboard outline with timing, 3. Interview segments and B-roll needs, 4. Suggested opening and closing shots, 5. Narrative arc across the video.",
                        tips: "Video is time-intensive—plan thoroughly before shooting. Think about pacing and visual variety. Claude provides good structural guidance. Always get b-roll—you'll need more than you think.",
                    },
                ],
            },
            {
                text: "Editing and post-production guidance",
                next: "recommendation",
                tools: [
                    {
                        name: "Video editing strategists",
                        description: "For making decisions about video structure, pacing, and storytelling flow.",
                        tools: ["Claude Sonnet 4", "ChatGPT o3"],
                        prompt: "I'm editing a video about [TOPIC]. I have these elements: [LIST FOOTAGE]. Help me: 1. Structure the video for maximum impact, 2. Decide pacing for different sections, 3. Suggest where to use music or natural sound, 4. Plan transitions between scenes, 5. Identify what might be cuttable if too long.",
                        tips: "ChatGPT o3 helps with logical structure. Kill your darlings—cut footage that doesn't serve the story. Vary pacing to maintain interest. Natural sound is powerful—don't over-rely on music.",
                    },
                ],
            },
        ],
    },
    multimedia_audio: {
        question: "What audio challenge do you have?",
        options: [
            {
                text: "Podcast structure and planning",
                next: "recommendation",
                tools: [
                    {
                        name: "Podcast planning assistants",
                        description: "For structuring podcast episodes and planning audio narratives.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "Help me plan a podcast episode about [TOPIC], length [DURATION]. Create: 1. Episode structure with segments and timing, 2. Cold open ideas, 3. Interview question flow, 4. Where to use music/effects, 5. How to build narrative tension and resolution.",
                        tips: "Audio is intimate and forgiving—conversational tone works. Claude excels at narrative structure. Plan for 'driveway moments'—compelling content that keeps listeners engaged. Build in variety—mix interviews, narration, and sound.",
                    },
                ],
            },
            {
                text: "Improving audio storytelling",
                next: "recommendation",
                tools: [
                    {
                        name: "Audio narrative enhancement",
                        description: "For strengthening audio storytelling through better writing and sound design.",
                        tools: ["Claude Sonnet 4", "Gemini 2.5 Pro"],
                        prompt: "Review my podcast script: [PASTE SCRIPT]. Help me: 1. Identify where pacing drags, 2. Suggest where to add sound elements or music, 3. Make narration more conversational and less written, 4. Find places to build tension or emotional moments.",
                        tips: "Write for the ear—read everything aloud. Claude helps identify clunky phrasing. Use the 'rule of threes' in lists. Strategic silence can be powerful. Sound design reinforces but shouldn't overwhelm story.",
                    },
                ],
            },
        ],
    },
    multimedia_interactive: {
        question: "What type of interactive story?",
        options: [
            {
                text: "Planning interactive features",
                next: "recommendation",
                tools: [
                    {
                        name: "Interactive storytelling planners",
                        description: "For conceptualizing interactive elements and user experiences.",
                        tools: ["Claude Sonnet 4", "ChatGPT o3"],
                        prompt: "I want to create an interactive story about [TOPIC]. Help me: 1. Identify which elements should be interactive and why, 2. Suggest user flow and navigation, 3. Plan how users will engage with data or media, 4. Consider mobile vs. desktop experience, 5. Determine technical complexity vs. impact.",
                        tips: "ChatGPT o3 helps think through complex user paths. Interactivity should serve the story, not just show off. Test with real users early. Consider accessibility—can all users access core content?",
                    },
                ],
            },
            {
                text: "Visualizing data or timelines",
                next: "recommendation",
                tools: [
                    {
                        name: "Visual narrative designers",
                        description: "For conceptualizing timelines, data visualizations, and visual storytelling.",
                        tools: ["Claude Sonnet 4", "ChatGPT 4o"],
                        prompt: "I want to visualize [DATA/TIMELINE/STORY] interactively. Help me: 1. Choose the right format (timeline, map, scrollytelling, etc.), 2. Decide what users should control vs. what's automated, 3. Plan key moments or reveals in the experience, 4. Suggest how to make complex information accessible.",
                        tips: "Claude excels at user experience thinking. Start with the story, then determine format—not the reverse. Progressive disclosure works well. Make sure the juice is worth the squeeze—simple can be better.",
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
