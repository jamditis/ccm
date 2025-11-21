# LLM Journalism Tool Advisor

An interactive decision tree application that helps journalists select the most appropriate AI/LLM tools for their specific journalism tasks.

![License](https://img.shields.io/badge/license-CC0%201.0-blue)
![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-5.2-646CFF?logo=vite)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

## 🎯 Overview

The LLM Journalism Tool Advisor guides journalists through a series of questions to recommend the most suitable AI tools (Claude, ChatGPT, Gemini, Perplexity, etc.) for their specific needs. Each recommendation includes:

- **Specific AI tools** best suited for the task
- **Sample prompts** that can be adapted and used immediately
- **Practical tips** for effective use
- **Ethical considerations** and limitations

## ✨ Features

### Complete Journalism Workflows

**📝 Content Creation & Writing**
- Article drafting and improvement
- Social media optimization (Twitter/X, LinkedIn)
- Long-form features and investigations
- Video and audio script writing

**📊 Data Analysis & Visualization**
- Dataset understanding and interpretation
- Statistical analysis and trend identification
- Visualization planning (charts, maps)
- Data storytelling for different audiences

**✏️ Editing & Refining**
- Structural editing and flow improvement
- Clarity and conciseness enhancement
- Grammar, style, and tone consistency
- Fact-checking and verification

**🎤 Source Finding & Management**
- Expert and source identification
- Interview preparation and strategy
- Source organization and tracking
- Credibility evaluation

**🎬 Multimedia Content**
- Photography planning and captions
- Video storyboarding and editing
- Podcast structure and audio storytelling
- Interactive features and data visualization

### Technical Features

- 🎨 **Modern UI** - Clean, responsive design with progress tracking
- 🔄 **State Management** - Efficient useReducer pattern
- 🛡️ **Error Handling** - Graceful error boundaries
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- ⚡ **Performance** - Optimized with memoization
- ♿ **Accessible** - ARIA labels and keyboard navigation
- 📦 **Lightweight** - ~60KB gzipped bundle

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
# Clone the repository
git clone https://github.com/jamditis/ccm.git
cd ccm

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
ccm/
├── components/              # React components
│   ├── ErrorBoundary.jsx   # Error handling wrapper
│   ├── Header.jsx           # Navigation and progress bar
│   ├── QuestionView.jsx     # Question display
│   ├── RecommendationView.jsx # Tool recommendations
│   └── ToolCard.jsx         # Individual tool cards
├── data/
│   └── decisionTree.js      # Decision tree configuration
├── utils/
│   ├── colorUtils.js        # Color mapping utilities
│   └── decisionReducer.js   # State management reducer
├── App.jsx                  # Main application component
├── App.css                  # Global styles
├── index.jsx                # Application entry point
└── package.json             # Project dependencies
```

## 🏗️ Architecture

### Component Hierarchy

```
<ErrorBoundary>
  <App>
    <Header />
    <QuestionView /> | <RecommendationView>
      <ToolCard />
    </QuestionView>
  </App>
</ErrorBoundary>
```

### State Management

The app uses React's `useReducer` hook for predictable state management:

- **State**: `{ currentStep, history, selectedTools, showRecommendation }`
- **Actions**: `SELECT_OPTION`, `GO_BACK`, `RESTART`

### Decision Tree Structure

The decision tree is defined in `data/decisionTree.js` with this structure:

```javascript
{
  nodeId: {
    question: "Question text",
    options: [
      {
        text: "Option text",
        next: "nextNodeId", // or "recommendation"
        tools: [/* tool recommendations */]
      }
    ]
  }
}
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed documentation.

## 🛠️ Development

### Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

### Adding New Recommendations

1. Edit `data/decisionTree.js`
2. Add your new node with question and options
3. Include tool recommendations with:
   - `name`: Tool category name
   - `description`: What it's used for
   - `tools`: Array of tool names
   - `prompt`: Sample prompt template
   - `tips`: Usage tips (optional)

Example:

```javascript
{
  text: "Your option",
  next: "recommendation",
  tools: [{
    name: "Tool Category",
    description: "What this helps with",
    tools: ["Claude Sonnet 4", "ChatGPT 4o"],
    prompt: "Your sample prompt here...",
    tips: "Helpful tips for users..."
  }]
}
```

### Code Style

- ESLint configured with React best practices
- PropTypes validation required for all components
- Functional components with hooks preferred
- Comments for complex logic

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Contribution Ideas

- 🌍 Add internationalization (i18n)
- 🧪 Add unit tests
- 📱 Improve mobile experience
- ♿ Enhance accessibility
- 🎨 Add dark mode toggle
- 💾 Add save/export functionality
- 🔍 Add search within recommendations

## 📝 License

This project is dedicated to the public domain under the [CC0 1.0 Universal](LICENSE) license.

## 👤 Author

Created by [Joe Amditis](https://twitter.com/jsamditis)

Last updated: June 2025

## 🙏 Acknowledgments

- Built with [React](https://reactjs.org/) and [Vite](https://vitejs.dev/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Refactored and enhanced with [Claude Code](https://claude.com/claude-code)

## 📊 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a detailed history of changes.

---

**Note**: This tool provides AI tool recommendations for journalism workflows. Always verify AI outputs and maintain journalistic standards. AI should assist, not replace, human judgment and reporting.
