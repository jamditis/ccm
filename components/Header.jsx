import React from "react";
import PropTypes from "prop-types";
import { calculateProgress } from "../utils/colorUtils";

/**
 * Header component with navigation, progress bar, and breadcrumb
 * @param {Object} props
 * @param {Array} props.history - Navigation history
 * @param {boolean} props.showRecommendation - Whether showing recommendations
 * @param {Function} props.onBack - Back button handler
 * @param {Function} props.onRestart - Restart button handler
 */
const Header = ({ history, showRecommendation, onBack, onRestart }) => {
    const progressPercentage = calculateProgress(history.length, showRecommendation);

    return (
        <div className="text-white p-4 sm:p-6">
            <div className="flex justify-between items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-bold">
                    LLM journalism tool advisor
                </h1>
                <div className="flex space-x-2 items-center flex-shrink-0">
                    <button
                        className={`p-2 rounded-full bg-black/20 hover:bg-black/30 ${
                            history.length === 0 ? "cursor-not-allowed opacity-50" : ""
                        }`}
                        onClick={onBack}
                        disabled={history.length === 0}
                        aria-label="Go back"
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
                        onClick={onRestart}
                        aria-label="Restart"
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

            {/* Progress Bar */}
            <div className="mt-4 bg-black/20 rounded-full h-2">
                <div
                    className="bg-white rounded-full h-2 transition-all duration-500 ease-in-out"
                    style={{ width: `${progressPercentage}%` }}
                ></div>
            </div>

            {/* Breadcrumb */}
            {history.length > 0 && (
                <div className="mt-3 flex flex-wrap items-center text-sm text-white/70">
                    {history.map((item, idx) => (
                        <React.Fragment key={idx}>
                            <span className="truncate">{item.selection}</span>
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
    );
};

Header.propTypes = {
    history: PropTypes.arrayOf(
        PropTypes.shape({
            step: PropTypes.string.isRequired,
            question: PropTypes.string.isRequired,
            selection: PropTypes.string.isRequired,
            tools: PropTypes.array,
        })
    ).isRequired,
    showRecommendation: PropTypes.bool.isRequired,
    onBack: PropTypes.func.isRequired,
    onRestart: PropTypes.func.isRequired,
};

export default Header;
