# ⚙️ Free tools from the Center for Cooperative Media

A collection of internal and external tools created by the [Center for Cooperative Media](https://centerforcooperativemedia.org/) at Montclair State University. These tools are designed to support local journalism operations, streamline administrative tasks, and help newsrooms leverage modern technology effectively.

## About the Center for Cooperative Media

The [Center for Cooperative Media](https://centerforcooperativemedia.org/) is a grant-funded program at the College  of Communication and Media at Montclair State University. Founded in 2012, the Center's mission is to **grow and strengthen local journalism and support an informed society** in New Jersey and beyond.

### What We Do

- **Coordinate statewide reporting** through the NJ News Commons, connecting 300+ local news providers
- **Provide training and support** to local journalists across New Jersey
- **Research collaborative journalism** and local news ecosystems
- **Develop innovative tools** to help newsrooms operate more efficiently
- **Host conferences** dedicated to studying collaborative journalism

The Center recently received a [$2.5 million Knight Foundation grant](https://www.montclair.edu/newscenter/2025/02/17/center-for-cooperative-media-receives-2-5m-knight-foundation-grant-to-expand-collaborative-journalism-nationwide/) to launch the Collaborative Journalism Resource Hub, supporting journalism collaboratives across the United States.

## Tools in This Repository

### LLM Journalism Tool Advisor | **Location**: [`/tools/ccm-app`](./tools/ccm-app)

![LLM Journalism Tool Advisor](https://i.imgur.com/DW3dNiy.png)

An interactive decision tree application that helps journalists select the most appropriate AI/LLM tools for their specific tasks. Features include:

- Guided workflow for content creation, data analysis, editing, source finding, and multimedia
- Tool recommendations for Claude, ChatGPT, Gemini, Perplexity, and more
- Sample prompts, practical tips, and ethical considerations
- Modern React UI with responsive design

**Tech Stack**: React 18, Vite, Tailwind CSS

[View Documentation →](./tools/ccm-app/README.md)

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

## Quick Start

### Browser-Based Tools

The **Invoicer** and **Sponsorship Generator** are single-file HTML applications that run directly in your browser:

1. Navigate to the tool directory
2. Open `index.html` in any modern web browser
3. Start using immediately—no installation required

### Node.js Applications

The **LLM Journalism Tool Advisor** requires Node.js:

```bash
# Navigate to the app directory
cd tools/ccm-app

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
├── tools/
│   ├── ccm-app/                        # LLM Journalism Tool Advisor
│   │   ├── components/                 # React components
│   │   ├── data/                       # Decision tree data
│   │   ├── utils/                      # Utility functions
│   │   ├── README.md                   # Tool documentation
│   │   └── ...
│   ├── invoicer/                       # Invoice Generator
│   │   ├── index.html                  # Single-file application
│   │   └── README.md                   # Tool documentation
│   └── sponsorship-generator/          # Sponsorship Package Generator
│       ├── index.html                  # Single-file application
│       └── README.md                   # Tool documentation
└── ...
```

## Author

**[Joe Amditis](https://twitter.com/jsamditis)**

Joe is the Associate Director of Operations at the Center for Cooperative Media and an adjunct professor in the College of Communication and Media at Montclair State University. He specializes in local news ecosystem management, collaborative journalism, and AI applications for journalism.

Joe is the author of several guides and educational resources for small and local newsrooms, including guides on generative AI. He is also the former producer and host of the [WTF Just Happened Today](https://wtfjht.com/) podcast and a veteran of the NJ Army National Guard.

- Email: amditisj@montclair.edu
- Twitter: [@jsamditis](https://twitter.com/jsamditis)
- Medium: [jamditis.medium.com](https://jamditis.medium.com/)

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
