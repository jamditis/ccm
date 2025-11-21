import React from "react";
import PropTypes from "prop-types";

/**
 * QuestionView component displays a question and its options
 * @param {Object} props
 * @param {string} props.question - The question to display
 * @param {Array} props.options - Array of option objects with text and next properties
 * @param {Function} props.onOptionSelect - Handler for option selection
 */
const QuestionView = ({ question, options, onOptionSelect }) => {
    return (
        <div>
            <h2 className="text-xl sm:text-2xl font-semibold mb-4 text-white">
                {question}
            </h2>
            <div className="space-y-3">
                {options.map((option, index) => (
                    <button
                        key={index}
                        className="w-full text-left p-4 rounded-lg bg-white/10 hover:bg-white/20 transition-all duration-200 flex justify-between items-center text-white"
                        onClick={() => onOptionSelect(option)}
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
                            aria-hidden="true"
                        >
                            <path d="m9 18 6-6-6-6" />
                        </svg>
                    </button>
                ))}
            </div>
        </div>
    );
};

QuestionView.propTypes = {
    question: PropTypes.string.isRequired,
    options: PropTypes.arrayOf(
        PropTypes.shape({
            text: PropTypes.string.isRequired,
            next: PropTypes.string.isRequired,
            tools: PropTypes.array,
        })
    ).isRequired,
    onOptionSelect: PropTypes.func.isRequired,
};

export default QuestionView;
