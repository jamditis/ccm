/**
 * State reducer for managing decision tree navigation
 * Consolidates all state management logic in one place
 */

export const initialState = {
    currentStep: "start",
    history: [],
    selectedTools: [],
    showRecommendation: false,
};

export const actionTypes = {
    SELECT_OPTION: "SELECT_OPTION",
    GO_BACK: "GO_BACK",
    RESTART: "RESTART",
};

/**
 * Reducer function for decision tree state management
 * @param {Object} state - Current state
 * @param {Object} action - Action with type and payload
 * @returns {Object} - New state
 */
export const decisionReducer = (state, action) => {
    switch (action.type) {
        case actionTypes.SELECT_OPTION: {
            const { option, currentQuestion, decisionTree } = action.payload;

            const newHistoryItem = {
                step: state.currentStep,
                question: currentQuestion,
                selection: option.text,
                tools: option.tools || [],
            };

            const newHistory = [...state.history, newHistoryItem];
            const newSelectedTools = option.tools
                ? [...state.selectedTools, ...option.tools]
                : state.selectedTools;

            return {
                ...state,
                history: newHistory,
                selectedTools: newSelectedTools,
                currentStep: option.next,
                showRecommendation: option.next === "recommendation",
            };
        }

        case actionTypes.GO_BACK: {
            if (state.history.length === 0) return state;

            const newHistory = [...state.history];
            const previous = newHistory.pop();

            // Rebuild selectedTools from remaining history
            const newSelectedTools = newHistory.reduce((acc, item) => {
                if (item.tools) {
                    return [...acc, ...item.tools];
                }
                return acc;
            }, []);

            return {
                ...state,
                history: newHistory,
                currentStep: previous.step,
                selectedTools: newSelectedTools,
                showRecommendation: false,
            };
        }

        case actionTypes.RESTART: {
            return initialState;
        }

        default:
            return state;
    }
};
