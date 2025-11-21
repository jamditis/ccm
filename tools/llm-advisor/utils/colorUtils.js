/**
 * Utility functions for color mapping based on step and tool types
 */

/**
 * Generic color mapping function
 * @param {string} key - The key to look up in the color map
 * @param {Object} colorMap - Map of keys to color classes
 * @returns {string} - Tailwind color class
 */
const getColorFromMap = (key, colorMap) => {
    const foundKey = Object.keys(colorMap).find((k) => key.startsWith(k));
    return colorMap[foundKey] || colorMap.default;
};

/**
 * Get color class for a decision tree step
 * @param {string} step - The current step in the decision tree
 * @returns {string} - Tailwind background color class
 */
export const getStepColor = (step) => {
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
    return getColorFromMap(step, colors);
};

/**
 * Get color class for an AI tool badge
 * @param {string} tool - The tool name
 * @returns {string} - Tailwind background and text color classes
 */
export const getToolColor = (tool) => {
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
    return getColorFromMap(tool, toolColors);
};

/**
 * Calculate progress percentage based on current position in decision tree
 * @param {number} historyLength - Number of completed steps
 * @param {boolean} showRecommendation - Whether showing final recommendation
 * @returns {number} - Progress percentage (0-100)
 */
export const calculateProgress = (historyLength, showRecommendation) => {
    if (showRecommendation) return 100;

    // Average depth of decision tree is approximately 3 steps
    const estimatedTotalSteps = 3;
    return Math.min(100, Math.round((historyLength / estimatedTotalSteps) * 100));
};
