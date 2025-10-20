import React from "react";
import PropTypes from "prop-types";

/**
 * Error Boundary component to catch and handle React errors gracefully
 * Prevents the entire app from crashing when a component error occurs
 */
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        console.error("Error caught by boundary:", error, errorInfo);
    }

    handleReset = () => {
        this.setState({ hasError: false, error: null });
        // Optionally reload the page
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 flex items-center justify-center">
                    <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 max-w-md text-center">
                        <h2 className="text-2xl font-bold text-white mb-4">
                            Oops! Something went wrong
                        </h2>
                        <p className="text-white/80 mb-6">
                            We encountered an unexpected error. Don&apos;t worry, your
                            progress hasn&apos;t been lost.
                        </p>
                        <button
                            onClick={this.handleReset}
                            className="px-6 py-3 bg-white/20 text-white rounded-lg hover:bg-white/30 transition-colors font-medium"
                        >
                            Restart Application
                        </button>
                        {process.env.NODE_ENV === "development" && this.state.error && (
                            <div className="mt-6 p-4 bg-black/30 rounded text-left">
                                <p className="text-red-400 text-sm font-mono">
                                    {this.state.error.toString()}
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

ErrorBoundary.propTypes = {
    children: PropTypes.node.isRequired,
};

export default ErrorBoundary;
