# Center for Cooperative Media - Tools & Projects

A collection of free tools and internal projects created by the [Center for Cooperative Media](https://centerforcooperativemedia.org/) at Montclair State University.

---

## What's in This Repository?

This repository contains **two main things**:

1. **Public Tools** (`/tools/`) - Free web-based tools designed to help journalists, newsrooms, and media organizations with everyday tasks like creating invoices, planning events, and choosing the right AI tools.

2. **Internal Research Projects** (`/social-scraper/`) - Research tools used by CCM staff for internal projects (not intended for public use).

If you're a **journalist or newsroom looking for tools**, head to the `/tools/` folder - everything there is free to use!

---

## About the Center for Cooperative Media

The [Center for Cooperative Media](https://centerforcooperativemedia.org/) is a grant-funded program at the College  of Communication and Media at Montclair State University. Founded in 2012, the Center's mission is to **grow and strengthen local journalism and support an informed society** in New Jersey and beyond.

### What We Do

- **Coordinate statewide reporting** through the NJ News Commons, connecting 300+ local news providers
- **Provide training and support** to local journalists across New Jersey
- **Research collaborative journalism** and local news ecosystems
- **Develop innovative tools** to help newsrooms operate more efficiently
- **Host conferences** dedicated to studying collaborative journalism

The Center recently received a [$2.5 million Knight Foundation grant](https://www.montclair.edu/newscenter/2025/02/17/center-for-cooperative-media-receives-2-5m-knight-foundation-grant-to-expand-collaborative-journalism-nationwide/) to launch the Collaborative Journalism Resource Hub, supporting journalism collaboratives across the United States.

## Public Tools

All tools in the `/tools/` folder are free to use. Most are single-file web applications that run directly in your browser - no installation required!

### LLM Journalism Tool Advisor | **Location**: [`/tools/llm-advisor`](./tools/llm-advisor)

![LLM Journalism Tool Advisor](https://i.imgur.com/DW3dNiy.png)

An interactive decision tree application that helps journalists select the most appropriate AI/LLM tools for their specific tasks. Features include:

- Guided workflow for content creation, data analysis, editing, source finding, and multimedia
- Tool recommendations for Claude, ChatGPT, Gemini, Perplexity, and more
- Sample prompts, practical tips, and ethical considerations
- Modern React UI with responsive design

**Tech Stack**: React 18, Vite, Tailwind CSS

[View Documentation →](./tools/llm-advisor/README.md)

---

### Invoicer | **Location**: [`/tools/invoicer`](./tools/invoicer)

![Invoicer tool](https://i.imgur.com/QHPpkqv.jpeg)

A professional invoice generator for creating beautiful, customizable invoices. Perfect for freelance journalists, consultants, and small newsrooms. Features include:

- Customizable themes (colors, fonts, corner styles)
- Logo upload and branding
- Profile saving for quick reuse
- PDF export
- Payment instructions support

**Tech Stack**: React 18, Tailwind CSS, html2pdf.js

[View Documentation →](./tools/invoicer/README.md)

---

### Sponsorship Package Generator | **Location**: [`/tools/sponsorship-generator`](./tools/sponsorship-generator)

![Sponsorship generator tool](https://i.imgur.com/lLMOTD5.jpeg)

A tool for creating professional sponsorship proposals and package overviews for events. Ideal for news organizations seeking sponsorships for events, programs, or initiatives. Features include:

- Generator mode for targeted proposals
- Builder mode to create/manage sponsorship tiers
- Support for cash and in-kind sponsorships
- PDF and PNG export
- Customizable event details and contact info

**Tech Stack**: React 18, Tailwind CSS, html2canvas, jsPDF

[View Documentation →](./tools/sponsorship-generator/README.md)

---

### Event Budget Calculator | **Location**: [`/tools/event-budget-calculator`](./tools/event-budget-calculator)

A comprehensive budget planning tool for events, helping newsrooms track expenses, revenue, and break-even analysis. Features include:

- Expense categories (venue, catering, A/V, marketing, staffing, materials)
- Revenue tracking (sponsorships, tickets, donations)
- Real-time calculations and summary dashboard
- Break-even analysis and coverage percentage
- Save/load multiple budgets
- PDF export

**Tech Stack**: React 18, Tailwind CSS, html2pdf.js

[View Documentation →](./tools/event-budget-calculator/README.md)

---

### Chart Maker | **Location**: [`/tools/chart-maker`](./tools/chart-maker)

A visual flowchart and diagram creation tool. Create professional charts with an intuitive drag-and-drop interface. Features include:

- Node-based chart building
- Multiple shape types (rectangles, diamonds, ovals)
- Customizable colors and styles
- Connection lines with drag-to-reconnect
- Export capabilities

**Tech Stack**: React 18, Tailwind CSS

---

### Media Kit Builder | **Location**: [`/tools/media-kit-builder`](./tools/media-kit-builder)

Create professional media kits to share with advertisers and sponsors. Present your audience data, ad rates, and platform information in a polished format.

**Tech Stack**: React 18, Tailwind CSS, html2pdf.js

[View Documentation →](./tools/media-kit-builder/README.md)

---

### Freelancer Rate Calculator | **Location**: [`/tools/freelancer-rate-calculator`](./tools/freelancer-rate-calculator)

Calculate fair freelance rates based on project type, complexity, and market benchmarks. Perfect for freelance journalists determining their rates.

**Tech Stack**: React 18, Tailwind CSS

[View Documentation →](./tools/freelancer-rate-calculator/README.md)

---

### Grant Proposal Generator | **Location**: [`/tools/grant-proposal-generator`](./tools/grant-proposal-generator)

Structure grant proposals with sections aligned to common journalism funder requirements. Includes templates for Knight Foundation, Google News Initiative, and more.

**Tech Stack**: React 18, Tailwind CSS, html2pdf.js

[View Documentation →](./tools/grant-proposal-generator/README.md)

---

### Collaboration Agreement Generator | **Location**: [`/tools/collaboration-agreement-generator`](./tools/collaboration-agreement-generator)

Create MOUs and collaboration agreements between news organizations for joint reporting projects, shared resources, or republishing arrangements.

**Tech Stack**: React 18, Tailwind CSS, html2pdf.js

[View Documentation →](./tools/collaboration-agreement-generator/README.md)

---

## Quick Start

### Browser-Based Tools

The **Invoicer**, **Sponsorship Generator**, and **Event Budget Calculator** are single-file HTML applications that run directly in your browser:

1. Navigate to the tool directory
2. Open `index.html` in any modern web browser
3. Start using immediately—no installation required

### Node.js Applications

The **LLM Journalism Tool Advisor** requires Node.js:

```bash
# Navigate to the app directory
cd tools/llm-advisor

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## Use Cases

### For Freelance Journalists
- Generate professional invoices for clients
- Select the right AI tools for reporting tasks
- Create sponsorship proposals for independent projects

### For Small Newsrooms
- Streamline invoice creation for contractors
- Train staff on AI tool selection
- Develop sponsorship packages for events and programs

### For News Organizations
- Standardize invoicing across the organization
- Guide journalists in responsible AI use
- Create consistent sponsorship materials

### For Event Organizers
- Build tiered sponsorship packages
- Generate customized proposals for prospects
- Export professional materials for distribution

## Contributing

We welcome contributions from the journalism community! Whether you're fixing bugs, adding features, or improving documentation, your help strengthens these tools for everyone.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Ideas

- Add new tool recommendations to the LLM Advisor
- Improve accessibility across all tools
- Add internationalization support
- Create additional export formats
- Enhance mobile responsiveness
- Write tests

## Technical Requirements

### Browser-Based Tools
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Internet connection (for CDN-loaded dependencies)

### Node.js Applications
- Node.js 16+
- npm or yarn

## Project Structure

```
ccm/
├── README.md                           # This file
├── docs/                               # Documentation and PRDs
│   ├── tool-prds.md                    # Product requirements for tools
│   └── ENHANCEMENTS.md                 # Technical enhancements documentation
├── tools/                              # PUBLIC TOOLS (free to use!)
│   ├── llm-advisor/                    # LLM Journalism Tool Advisor (React app)
│   ├── invoicer/                       # Invoice Generator
│   ├── sponsorship-generator/          # Sponsorship Package Generator
│   ├── event-budget-calculator/        # Event Budget Calculator
│   ├── chart-maker/                    # Flowchart/Diagram Creator
│   ├── media-kit-builder/              # Media Kit Builder
│   ├── freelancer-rate-calculator/     # Freelance Rate Calculator
│   ├── grant-proposal-generator/       # Grant Proposal Outline Tool
│   ├── collaboration-agreement-generator/  # MOU/Agreement Generator
│   └── shared/                         # Shared utilities and components
└── social-scraper/                     # INTERNAL: Research project (not for public use)
```

## Author

Created by the [Center for Cooperative Media](https://centerforcooperativemedia.org/) at Montclair State University.

For inquiries, contact: [info@centerforcooperativemedia.org](mailto:info@centerforcooperativemedia.org)

## License

These tools are provided by the Center for Cooperative Media for use in supporting local journalism and media organizations. Individual tools may have specific license information in their respective directories.

## Acknowledgments

- [Montclair State University](https://www.montclair.edu/) - Institutional home of the Center
- [Knight Foundation](https://knightfoundation.org/) - Funding support for collaborative journalism initiatives
- The NJ News Commons partners and the broader local journalism community

## Related Resources

- [Center for Cooperative Media](https://centerforcooperativemedia.org/) - Our main website
- [Collaborative Journalism](https://collaborativejournalism.org/) - Resources on collaborative journalism
- [NJ News Commons](https://centerforcooperativemedia.org/nj-news-commons/) - Our flagship project connecting NJ news providers
- [CCM Research & Reports](https://centerforcooperativemedia.org/portfolio-item/research/) - Our published research

---

**Note**: These tools are designed to assist journalists and news organizations in their work. For AI-related tools, always verify AI outputs and maintain journalistic standards. AI should assist, not replace, human judgment and reporting.
