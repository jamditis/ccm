# Freelancer Rate Calculator

A calculator to help freelance journalists determine fair rates based on project type, complexity, rights, turnaround, and market benchmarks. Outputs professional rate quotes.

## Features

### Core Functionality
- **Project Type Selection**: Article, photo essay, video, podcast, social content, editing
- **Rate Calculation Methods**: Per word, per hour, per project, day rate
- **Complexity Factors**: Research depth, travel, specialized expertise, number of interviews
- **Rights & Licensing**: FNASR, exclusive (limited/perpetual), work-for-hire
- **Market Benchmarks**: Reference rates from industry surveys

### Calculations
- Base rate calculation with quantity
- Complexity multipliers (research, travel, expertise, interviews)
- Rush fee additions (standard, 1 week, 48hr, 24hr)
- Rights premiums
- Kill fee recommendations (33% of total)
- Expense tracking

### Output
- Real-time rate breakdown summary
- Market position indicator
- Professional quote template generation
- Copy to clipboard functionality
- PDF export

## Quick Start

1. Open `index.html` in any modern web browser
2. Select your project type
3. Enter your base rate and quantity
4. Adjust complexity factors as needed
5. Set turnaround and rights
6. Add any expenses
7. View your calculated rate and generate a quote

## Technical Details

### Dependencies (loaded via CDN)
- React 18
- Tailwind CSS
- html2pdf.js
- Google Fonts (Inter, JetBrains Mono)

### Data Persistence
- Rate profiles saved to browser localStorage
- No server required - works entirely offline

### Browser Support
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile responsive design

## Market Benchmarks

The calculator includes industry benchmarks based on 2024 journalism rate surveys:

| Project Type | Low | Median | High | Premium |
|-------------|-----|--------|------|---------|
| Article | $0.25/word | $0.50/word | $1.50/word | $2.50/word |
| Photo | $150/assignment | $350/assignment | $750/assignment | $1,500/assignment |
| Video | $500/project | $1,500/project | $3,500/project | $7,500/project |
| Podcast | $200/episode | $500/episode | $1,200/episode | $2,500/episode |
| Social | $50/package | $150/package | $400/package | $800/package |
| Editing | $35/hour | $65/hour | $125/hour | $200/hour |

## Multipliers

### Research Depth
- Light: 1.0x (basic research)
- Moderate: 1.25x (multiple sources, some interviews)
- Deep: 1.5x (extensive research, data analysis)

### Additional Factors
- Travel Required: +15%
- Specialized Expertise: +20%
- Interviews: +5% each (max 25%)

### Turnaround
- Standard (1-2 weeks): 1.0x
- Rush (1 week): 1.25x
- Rush (48hr): 1.5x
- Rush (24hr): 2.0x

### Rights
- FNASR: 1.0x
- Exclusive (Limited): 1.5x
- Exclusive (Perpetual): 2.0x
- Work for Hire: 2.5x

## License

This tool is provided by the Center for Cooperative Media under CC0 1.0 (public domain).

## Author

Created by Joe Amditis for the Center for Cooperative Media.
