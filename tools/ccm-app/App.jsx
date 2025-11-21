import React, { useReducer, useMemo, useCallback } from "react";
import "./App.css";
import { decisionTree } from "./data/decisionTree";
import { getStepColor } from "./utils/colorUtils";
import { decisionReducer, initialState, actionTypes } from "./utils/decisionReducer";
import Header from "./components/Header";
import QuestionView from "./components/QuestionView";
import RecommendationView from "./components/RecommendationView";

const App = () => {
    const [state, dispatch] = useReducer(decisionReducer, initialState);
    const { currentStep, history, selectedTools, showRecommendation } = state;

    // Memoize current node to avoid recalculation
    const currentNode = useMemo(
        () => decisionTree[currentStep],
        [currentStep]
    );

    // Memoize color class
    const colorClass = useMemo(
        () => getStepColor(currentStep),
        [currentStep]
    );

    // Event handlers with useCallback for performance
    const handleOptionSelect = useCallback(
        (option) => {
            dispatch({
                type: actionTypes.SELECT_OPTION,
                payload: {
                    option,
                    currentQuestion: currentNode.question,
                    decisionTree,
                },
            });
        },
        [currentNode]
    );

    const handleBack = useCallback(() => {
        dispatch({ type: actionTypes.GO_BACK });
    }, []);

    const handleRestart = useCallback(() => {
        dispatch({ type: actionTypes.RESTART });
    }, []);

    // Memoize the main content view
    const mainContent = useMemo(() => {
        if (showRecommendation) {
            return (
                <RecommendationView
                    selectedTools={selectedTools}
                    onRestart={handleRestart}
                />
            );
        }

        return (
            <QuestionView
                question={currentNode.question}
                options={currentNode.options}
                onOptionSelect={handleOptionSelect}
            />
        );
    }, [showRecommendation, selectedTools, currentNode, handleOptionSelect, handleRestart]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
            <div
                className={`${colorClass} rounded-lg shadow-2xl max-w-4xl mx-auto overflow-hidden`}
            >
                {/* Header with Progress and Navigation */}
                <Header
                    history={history}
                    showRecommendation={showRecommendation}
                    onBack={handleBack}
                    onRestart={handleRestart}
                />

                {/* Main Content */}
                <div className="p-4 sm:p-6">{mainContent}</div>

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
