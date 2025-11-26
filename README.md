# Center for Cooperative Media - Tools & Projects

A collection of **free tools** for journalists and newsrooms, created by the [Center for Cooperative Media](https://centerforcooperativemedia.org/) at Montclair State University.

> 🎯 **Just looking for tools to use?** Skip to [Public Tools](#public-tools) below. Everything is free!

---

## What's in This Repository?

A "repository" is simply a collection of files and folders stored online (like a shared folder on Google Drive, but for code). This one contains:

### 1. 🛠️ Public Tools (for everyone!)
**Location:** `/tools/` folder

Nine free browser-based tools that help with everyday journalism tasks:
- Creating professional invoices
- Building sponsorship proposals
- Planning event budgets
- Finding the right AI tools for your work
- And more...

**No installation required!** Most tools work by simply opening a file in your web browser (like Chrome, Safari, or Firefox).

### 2. 🔬 Internal Research Projects (staff only)
**Location:** `/social-scraper/` folder

Research tools used by CCM staff. Not intended for public use, but the code is visible here for transparency.

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

**What it does:** Answers the question "Which AI tool should I use?" through a simple question-and-answer format. Like a quiz that leads you to the right tool for your journalism task.

**Features:**
- Step-by-step guidance for writing, data analysis, editing, research, and multimedia
- Recommendations for popular AI tools (Claude, ChatGPT, Gemini, Perplexity)
- Ready-to-use prompts and ethical guidelines
- Works on phones, tablets, and computers

**How to use:** This tool requires a few extra steps to run (see [Quick Start](#nodejs-applications) below).

[View Documentation →](./tools/llm-advisor/README.md)

---

### Invoicer | **Location**: [`/tools/invoicer`](./tools/invoicer)

![Invoicer tool](https://i.imgur.com/QHPpkqv.jpeg)

**What it does:** Creates professional invoices you can send to clients. Just fill in the blanks and download a PDF.

**Features:**
- Customize colors, fonts, and styles to match your brand
- Add your logo
- Save your info so you don't have to re-enter it each time
- Download as a PDF ready to email
- Include payment instructions (Venmo, bank transfer, etc.)

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/invoicer/README.md)

---

### Sponsorship Package Generator | **Location**: [`/tools/sponsorship-generator`](./tools/sponsorship-generator)

![Sponsorship generator tool](https://i.imgur.com/lLMOTD5.jpeg)

**What it does:** Creates professional sponsorship proposals for events. Perfect for pitching sponsors like "Gold," "Silver," and "Bronze" packages.

**Features:**
- **Generator mode:** Create targeted proposals for specific sponsors
- **Builder mode:** Design your own sponsorship tiers with custom benefits
- Handle both cash sponsorships and "in-kind" donations (like free venue space)
- Download as PDF (for emailing) or PNG image (for social media)
- Add your event details and contact information

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/sponsorship-generator/README.md)

---

### Event Budget Calculator | **Location**: [`/tools/event-budget-calculator`](./tools/event-budget-calculator)

**What it does:** Helps you plan and track event finances. See at a glance if your revenue covers your costs.

**Features:**
- Track expenses by category: venue, food, equipment, marketing, staff, supplies
- Track income from sponsorships, ticket sales, and donations
- See totals update automatically as you enter numbers
- **Break-even analysis:** Shows how much of your costs are covered
- Save multiple budgets and come back to them later
- Download as a PDF

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/event-budget-calculator/README.md)

---

### Chart Maker | **Location**: [`/tools/chart-maker`](./tools/chart-maker)

**What it does:** Creates flowcharts and diagrams by dragging and dropping shapes. Great for visualizing processes or organizational structures.

**Features:**
- Drag-and-drop shapes to build your chart
- Multiple shape types: boxes, diamonds (for decisions), ovals
- Customize colors and styles
- Draw lines to connect shapes
- Export your finished chart

**How to use:** Just open the file in your web browser—no installation needed!

---

### Media Kit Builder | **Location**: [`/tools/media-kit-builder`](./tools/media-kit-builder)

**What it does:** Creates a professional "media kit"—a document that tells advertisers about your audience and ad rates. Essential for selling ads.

**Features:**
- Present your audience size and demographics
- List your ad rates and options
- Showcase your platforms (website, newsletter, social media, podcast)
- Professional formatting that looks polished
- Download as a PDF

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/media-kit-builder/README.md)

---

### Freelancer Rate Calculator | **Location**: [`/tools/freelancer-rate-calculator`](./tools/freelancer-rate-calculator)

**What it does:** Helps freelancers figure out how much to charge. Answers "What's a fair rate for this project?"

**Features:**
- Choose your project type (article, photo, video, podcast, etc.)
- Factor in complexity, rush deadlines, and usage rights
- See how your rate compares to industry standards
- Get a professional quote you can send to clients

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/freelancer-rate-calculator/README.md)

---

### Grant Proposal Generator | **Location**: [`/tools/grant-proposal-generator`](./tools/grant-proposal-generator)

**What it does:** Helps you write grant proposals by providing a structured outline with all the sections funders typically require.

**Features:**
- Templates for major journalism funders (Knight Foundation, Google News Initiative, etc.)
- Section-by-section guidance telling you what to write
- Word count tracking to stay within limits
- Progress tracking so you know what's done
- Download your proposal as a PDF

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/grant-proposal-generator/README.md)

---

### Collaboration Agreement Generator | **Location**: [`/tools/collaboration-agreement-generator`](./tools/collaboration-agreement-generator)

**What it does:** Creates formal agreements between news organizations working together. Think of it as a fill-in-the-blank contract generator.

**Features:**
- Templates for different collaboration types:
  - Joint investigations
  - Content sharing/republishing
  - Shared resources (staff, equipment)
  - Event partnerships
- Support for 2 or more partner organizations
- Cover all the important topics: who does what, editorial standards, credit, finances
- Download a professional PDF ready for signatures

**How to use:** Just open the file in your web browser—no installation needed!

[View Documentation →](./tools/collaboration-agreement-generator/README.md)

---

## Quick Start

### 🌐 Browser-Based Tools (Most Tools)

Most tools work instantly in your web browser. Here's how:

**Option A: Download and Open (Easiest)**
1. Download the `index.html` file from the tool's folder
2. Double-click the file to open it in your web browser
3. Start using—that's it!

**Option B: Open Directly from GitHub**
1. Navigate to the tool's folder on GitHub
2. Click on `index.html`
3. Click the "Raw" button, then save the page
4. Open the saved file in your browser

**Tools that work this way:**
- Invoicer
- Sponsorship Package Generator
- Event Budget Calculator
- Chart Maker
- Media Kit Builder
- Freelancer Rate Calculator
- Grant Proposal Generator
- Collaboration Agreement Generator

---

### 💻 Node.js Applications (LLM Advisor Only)

The **LLM Journalism Tool Advisor** is more complex and requires some technical setup. If you're not comfortable with command-line tools, ask a tech-savvy colleague for help.

**What you need first:**
- Node.js installed on your computer (download free from [nodejs.org](https://nodejs.org))

**Steps:**
```bash
# 1. Open your computer's Terminal (Mac) or Command Prompt (Windows)

# 2. Navigate to the app folder
cd tools/llm-advisor

# 3. Install the required software (only needed once)
npm install

# 4. Start the tool
npm run dev
```

After running these commands, open your web browser and go to: `http://localhost:5173`

> **Tip:** "npm" is a tool that comes with Node.js for managing software packages. The commands above download required components and start the application.

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

### For Browser-Based Tools (Most Users)
You just need:
- A modern web browser (Chrome, Firefox, Safari, or Edge)
- JavaScript enabled (it usually is by default)
- Internet connection for the first load (some features are downloaded from the web)

That's it! No special software to install.

### For the LLM Advisor Tool (Technical Users)
- **Node.js** version 16 or newer ([free download](https://nodejs.org))
- **npm** (comes automatically with Node.js)

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

## Glossary: Technical Terms Explained

New to tech? Here's what some of the technical terms in this repository mean:

| Term | What It Means |
|------|---------------|
| **Repository (Repo)** | A folder that stores code and files online, like a shared Google Drive but for programmers |
| **Browser** | The app you use to visit websites (Chrome, Safari, Firefox, Edge) |
| **HTML** | The language used to create web pages. Files ending in `.html` can be opened in any browser |
| **PDF** | A document format that looks the same on any computer. Great for sharing professional documents |
| **Node.js** | Free software that lets you run JavaScript programs on your computer (not just in a browser) |
| **npm** | A tool that downloads and installs software packages. Comes with Node.js |
| **LLM** | Large Language Model—the technology behind AI assistants like ChatGPT and Claude |
| **API** | Application Programming Interface—a way for software programs to talk to each other |
| **Open Source** | Software whose code is publicly available for anyone to see, use, and improve |
| **GitHub** | A website for storing and sharing code (where this repository lives) |
| **localhost** | Your own computer, when it's running a web server. "localhost:5173" means a website running on your machine |
| **Terminal/Command Line** | A text-based way to control your computer by typing commands |

---

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
