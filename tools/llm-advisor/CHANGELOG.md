# Changelog

All notable changes to the LLM Journalism Tool Advisor project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite (README, ARCHITECTURE, CONTRIBUTING, CHANGELOG)

## [2.0.0] - 2025-01-XX

Major refactoring and feature completion across three phases.

### Phase 3: Enhancement & Completion

#### Added
- Complete decision tree with all 5 missing journalism workflow branches
  - Content Creation & Writing (8 tool recommendations)
  - Data Analysis & Visualization (8 tool recommendations)
  - Editing & Refining (8 tool recommendations)
  - Source Finding & Management (8 tool recommendations)
  - Multimedia Content (8 tool recommendations)
- ErrorBoundary component for graceful error handling
- 30+ unique tool recommendations across all journalism workflows
- Detailed sample prompts for each recommendation
- Practical tips and ethical considerations
- Support for social media content creation (Twitter, LinkedIn)
- Long-form narrative structure guidance
- Video and audio script writing assistance
- Data visualization planning tools
- Statistical analysis recommendations
- Interview preparation strategies
- Fact-checking and verification workflows
- Podcast and multimedia production guidance

#### Changed
- Decision tree expanded from 74 to 743 lines
- Bundle size increased from 154KB to 187KB (necessary for complete functionality)

#### Technical
- Added error boundary with user-friendly error messages
- Dev mode error details for debugging
- Graceful degradation on component errors

### Phase 2: Architecture Improvements

#### Added
- Modular component structure with clear separation of concerns
- `components/` directory with 5 focused components:
  - Header.jsx (navigation and progress tracking)
  - QuestionView.jsx (question display)
  - RecommendationView.jsx (recommendations container)
  - ToolCard.jsx (individual tool cards)
- `data/` directory for decision tree configuration
- `utils/` directory for helper functions:
  - colorUtils.js (color mapping functions)
  - decisionReducer.js (state management)
- PropTypes validation for all components
- Performance optimizations:
  - useMemo for computed values
  - useCallback for event handlers
  - Memoized component rendering
- Comprehensive JSDoc documentation

#### Changed
- App.jsx refactored from 414 lines to 107 lines (74% reduction)
- State management migrated from multiple useState to single useReducer
- Color mapping functions consolidated into reusable utilities
- Progress calculation made dynamic

#### Removed
- Inline component definitions
- Duplicate state management logic
- Redundant helper functions

#### Technical
- Build time: ~1.4s (stable)
- Lint: 0 errors, 0 warnings
- Bundle: 154KB → 187KB (with all features)

### Phase 1: Quick Wins

#### Added
- Proper Tailwind CSS configuration with correct content paths
- Dynamic progress calculation showing 100% at completion

#### Changed
- App.css reduced from 892 to 123 lines (86% reduction)
- Fixed progress bar to show accurate completion percentage
- Updated Tailwind config to scan root-level files

#### Removed
- Unused dependencies:
  - @aws-sdk/client-s3 (~6MB)
  - mime-types
  - vanilla-tilt
- LLM-tool-advisor.zip file (6.5MB)
- Unused CSS classes:
  - .glass-card
  - .modal and modal-related styles
  - .tool-card
  - .case-study-card
  - Dark mode theme styles (not implemented)
  - 600+ lines of unused styles

#### Fixed
- Progress calculation using hardcoded values
- Tailwind not detecting utility classes
- CSS bloat from unused styles

#### Technical
- Reduced total codebase by ~4,000 lines
- Removed ~6-7MB of unused dependencies
- Build time: ~1.3s
- Lint: 0 errors, 0 warnings

## [1.0.0] - 2025-06-XX

Initial release of the LLM Journalism Tool Advisor.

### Added
- Basic decision tree with research workflow
- Interactive question and answer interface
- Tool recommendations for basic research tasks
- Progress tracking
- Responsive design
- React + Vite + Tailwind CSS stack

### Features
- Start node with 6 main journalism task categories
- Research branch with 2 complete paths:
  - General knowledge topics
  - Niche/specialized subjects
- Basic UI with gradient background
- Navigation controls (back, restart)
- Color-coded steps

## Comparison: Before & After

### Code Metrics

| Metric | v1.0.0 | v2.0.0 | Change |
|--------|--------|--------|--------|
| App.jsx | 414 lines | 107 lines | -74% |
| App.css | 892 lines | 123 lines | -86% |
| Components | 1 file | 5 files | +400% |
| Decision paths | 2 paths | 30+ paths | +1400% |
| Dependencies | 5 packages | 3 packages | -40% |
| Bundle size | 151 KB | 187 KB | +24% |
| User workflows | 1 complete | 6 complete | +500% |

### Functionality

**v1.0.0:**
- Research workflow only
- 2 recommendation paths
- No error handling
- Monolithic component
- Basic UI

**v2.0.0:**
- All 6 journalism workflows
- 30+ recommendation paths
- Error boundary
- Modular architecture
- Optimized performance
- Production-ready

## Migration Guide

### From v1.0.0 to v2.0.0

No breaking changes for end users. The app maintains the same interface and behavior, with expanded functionality.

For developers:

1. **Component imports** - Update imports if extending:
   ```javascript
   // Old
   import App from './App';

   // New - specific components available
   import Header from './components/Header';
   import ToolCard from './components/ToolCard';
   ```

2. **Decision tree** - Now in separate file:
   ```javascript
   // Old - inline in App.jsx
   const decisionTree = { ... }

   // New - imported from data
   import { decisionTree } from './data/decisionTree';
   ```

3. **State management** - Changed to useReducer:
   ```javascript
   // Old
   const [currentStep, setCurrentStep] = useState("start");
   const [history, setHistory] = useState([]);

   // New
   const [state, dispatch] = useReducer(decisionReducer, initialState);
   const { currentStep, history } = state;
   ```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to contribute to this project.

## Links

- [Repository](https://github.com/jamditis/ccm)
- [Issues](https://github.com/jamditis/ccm/issues)
- [Pull Requests](https://github.com/jamditis/ccm/pulls)

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes
- `Technical` - Technical details
