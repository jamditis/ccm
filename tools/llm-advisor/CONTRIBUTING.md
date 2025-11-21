# Contributing to LLM Journalism Tool Advisor

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Adding Content](#adding-content)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize journalism ethics and accuracy
- Welcome diverse perspectives
- Support learning and growth

### Not Acceptable

- Harassment or discriminatory language
- Trolling or inflammatory comments
- Sharing private information without permission
- Unprofessional conduct

## Getting Started

### Prerequisites

- Node.js 16 or higher
- npm or yarn
- Git
- A code editor (VS Code recommended)

### Initial Setup

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/ccm.git
cd ccm

# Install dependencies
npm install

# Start development server
npm run dev

# Run linter
npm run lint
```

## Development Workflow

### Branch Strategy

1. Create a branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. Make your changes

3. Test thoroughly:
   ```bash
   npm run build   # Verify build succeeds
   npm run lint    # Verify no lint errors
   ```

4. Commit with clear messages:
   ```bash
   git commit -m "Add: Description of your changes"
   # or "Fix:", "Update:", "Remove:", etc.
   ```

5. Push to your fork:
   ```bash
   git push origin your-branch-name
   ```

6. Open a Pull Request

### Commit Message Format

```
<Type>: <Short description>

<Optional longer description>

<Optional footer>
```

**Types:**
- `Add`: New feature or content
- `Fix`: Bug fix
- `Update`: Modify existing feature
- `Remove`: Delete code or features
- `Refactor`: Code improvement without changing functionality
- `Docs`: Documentation changes
- `Style`: Formatting changes (no code changes)
- `Test`: Add or modify tests

**Examples:**
```
Add: New data visualization recommendations

Expand decision tree with 4 new visualization options for
journalists working with charts, maps, and infographics.

Add: Social media content branch in decision tree
Fix: Progress bar not showing 100% at completion
Update: Improve sample prompts for interview preparation
Docs: Add architecture documentation
```

## Coding Standards

### JavaScript/React Style

1. **Use functional components** with hooks (no class components except ErrorBoundary)

2. **PropTypes validation** required for all components:
   ```javascript
   import PropTypes from 'prop-types';

   MyComponent.propTypes = {
     data: PropTypes.array.isRequired,
     onClick: PropTypes.func.isRequired
   };
   ```

3. **Destructure props** in function parameters:
   ```javascript
   // Good
   const MyComponent = ({ data, onClick }) => { ... }

   // Avoid
   const MyComponent = (props) => {
     const data = props.data;
     ...
   }
   ```

4. **Use memoization** for expensive computations:
   ```javascript
   const value = useMemo(() => computeExpensiveValue(a, b), [a, b]);
   const callback = useCallback(() => doSomething(a), [a]);
   ```

5. **Name event handlers** with `handle` prefix:
   ```javascript
   const handleClick = () => { ... }
   const handleSubmit = () => { ... }
   ```

### File Organization

- One component per file
- Export component as default
- Group related files in directories
- Keep components under 300 lines

### CSS/Styling

- Use Tailwind utilities when possible
- Custom CSS only for animations or complex styles
- Keep App.css minimal
- Follow mobile-first responsive design

### ESLint

All code must pass ESLint with zero errors:

```bash
npm run lint
```

Fix issues before committing. Common issues:
- Missing PropTypes
- Unused variables
- Unescaped characters in JSX

## Adding Content

### Adding Tool Recommendations

To add new AI tool recommendations to the decision tree:

1. **Open** `data/decisionTree.js`

2. **Find or create** the appropriate node

3. **Add your recommendation** following this structure:

```javascript
{
  text: "Your option text",
  next: "recommendation",  // or another node ID
  tools: [{
    name: "Tool Category Name",
    description: "Clear description of what this helps with",
    tools: ["Tool Name 1", "Tool Name 2"],
    prompt: "Sample prompt with [PLACEHOLDERS] for user to fill in...",
    tips: "Practical tips for using these tools effectively..."
  }]
}
```

4. **Test the path** by running the app and clicking through

5. **Verify** all text is clear and error-free

### Content Guidelines

**Tool Recommendations:**
- Focus on journalism-specific use cases
- Provide concrete, actionable prompts
- Include realistic tips from actual usage
- Mention limitations and ethical considerations
- Verify tool names and capabilities are current

**Sample Prompts:**
- Use clear [PLACEHOLDERS] for user input
- Be specific about desired output
- Include context about audience/purpose
- Provide structural guidance (numbered steps, etc.)
- Keep under 150 words when possible

**Tips:**
- Share practical wisdom from real use
- Warn about common pitfalls
- Suggest ways to verify AI outputs
- Mention when human expertise is essential
- Keep under 75 words

### Adding New Decision Branches

To add a new branch to the decision tree:

1. **Plan the flow**:
   - What question starts this branch?
   - What options does the user have?
   - How many levels deep?
   - Where does it lead to recommendations?

2. **Create nodes** in `decisionTree.js`:
   ```javascript
   new_branch: {
     question: "Your question?",
     options: [
       { text: "Option 1", next: "new_branch_sub1" },
       { text: "Option 2", next: "new_branch_sub2" }
     ]
   },
   new_branch_sub1: {
     // ...
   }
   ```

3. **Link from main menu**:
   ```javascript
   start: {
     question: "What journalism task are you working on today?",
     options: [
       // ... existing options
       { text: "Your new task", next: "new_branch" }
     ]
   }
   ```

4. **Test thoroughly** - Click through all paths

5. **Update README** if adding major functionality

## Pull Request Process

### Before Submitting

- [ ] Code builds successfully (`npm run build`)
- [ ] Linting passes (`npm run lint`)
- [ ] Changes tested manually in browser
- [ ] All paths through decision tree work
- [ ] PropTypes added for any new components
- [ ] No console errors or warnings
- [ ] README updated if needed
- [ ] Commit messages follow format

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Content addition
- [ ] Documentation update
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How did you test these changes?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Build passes
- [ ] Lint passes
- [ ] Tested manually
- [ ] PropTypes added
- [ ] Documentation updated
```

### Review Process

1. Maintainer reviews PR
2. Feedback provided if changes needed
3. You address feedback
4. Maintainer approves and merges
5. Your contribution is live!

## Reporting Issues

### Bug Reports

Use this template:

```markdown
**Describe the bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment**
- Browser: [e.g., Chrome 118]
- OS: [e.g., macOS 14]
- Device: [e.g., Desktop]

**Additional context**
Any other relevant information
```

### Feature Requests

Use this template:

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired feature

**Describe alternatives**
Other solutions you've considered

**Additional context**
Any other information, mockups, examples
```

## Questions?

- Open an issue for questions about contributing
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details
- Check existing issues and PRs for similar work

## License

By contributing, you agree that your contributions will be licensed under the CC0 1.0 Universal license.

---

Thank you for contributing to help journalists use AI tools more effectively!
