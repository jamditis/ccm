import React from "react";
import PropTypes from "prop-types";
import { getToolColor } from "../utils/colorUtils";

/**
 * ToolCard component displays a single tool recommendation
 * @param {Object} props
 * @param {Object} props.tool - Tool object with name, description, tools, prompt, and tips
 */
const ToolCard = ({ tool }) => {
    return (
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 sm:p-5">
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
                    aria-hidden="true"
                >
                    <path d="M12 20s-8-4.5-8-12.5A8 8 0 0 1 12 4a8 8 0 0 1 8 8.5c0 8-8 12.5-8 12.5z" />
                    <circle cx="12" cy="11" r="2" />
                </svg>
                {tool.name}
            </h3>
            <p className="mt-2 text-white/80">{tool.description}</p>

            {/* Recommended Tools */}
            <div className="mt-4">
                <h4 className="font-medium text-white">Recommended tools:</h4>
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

            {/* Sample Prompt */}
            <div className="mt-4 p-3 sm:p-4 bg-black/20 rounded border border-white/20">
                <h4 className="font-medium text-white">Sample prompt:</h4>
                <code className="block mt-1 text-sm whitespace-pre-wrap text-white/90">
                    {tool.prompt}
                </code>
            </div>

            {/* Tips */}
            {tool.tips && (
                <div className="mt-4">
                    <h4 className="font-medium text-white">Tips:</h4>
                    <p className="mt-1 text-white/80 text-sm">{tool.tips}</p>
                </div>
            )}
        </div>
    );
};

ToolCard.propTypes = {
    tool: PropTypes.shape({
        name: PropTypes.string.isRequired,
        description: PropTypes.string.isRequired,
        tools: PropTypes.arrayOf(PropTypes.string).isRequired,
        prompt: PropTypes.string.isRequired,
        tips: PropTypes.string,
    }).isRequired,
};

export default ToolCard;
