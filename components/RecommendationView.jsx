import React from "react";
import PropTypes from "prop-types";
import ToolCard from "./ToolCard";

/**
 * RecommendationView component displays tool recommendations
 * @param {Object} props
 * @param {Array} props.selectedTools - Array of recommended tool objects
 * @param {Function} props.onRestart - Handler for restart button
 */
const RecommendationView = ({ selectedTools, onRestart }) => {
    return (
        <div>
            <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-white">
                Your recommended tools and approaches
            </h2>
            <div className="space-y-6">
                {selectedTools.map((tool, index) => (
                    <ToolCard key={index} tool={tool} />
                ))}
            </div>
            <div className="mt-6">
                <button
                    className="px-4 py-2 bg-white/20 text-white rounded-lg hover:bg-white/30 transition-colors"
                    onClick={onRestart}
                >
                    Start another task
                </button>
            </div>
        </div>
    );
};

RecommendationView.propTypes = {
    selectedTools: PropTypes.arrayOf(
        PropTypes.shape({
            name: PropTypes.string.isRequired,
            description: PropTypes.string.isRequired,
            tools: PropTypes.arrayOf(PropTypes.string).isRequired,
            prompt: PropTypes.string.isRequired,
            tips: PropTypes.string,
        })
    ).isRequired,
    onRestart: PropTypes.func.isRequired,
};

export default RecommendationView;
