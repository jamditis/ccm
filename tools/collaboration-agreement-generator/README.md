# Collaboration Agreement Generator

Create MOUs (Memoranda of Understanding) or collaboration agreements between news organizations for joint reporting projects, shared resources, or republishing arrangements.

## Features

### Core Functionality
- **Agreement Types**: 5 pre-built templates for common collaboration scenarios
- **Multi-Party Support**: Add 2+ organizations with contact details
- **Section Builder**: Standard legal/agreement sections with boilerplate text
- **Custom Clauses**: Add your own sections as needed
- **Signature Blocks**: Professional signature lines for all parties

### Agreement Types
- **Shared Reporting Project**: For joint investigations or reporting
- **Content Sharing/Republishing**: For syndication arrangements
- **Resource Sharing**: For sharing staff, equipment, or data
- **Event Co-hosting**: For jointly organized events
- **General Partnership MOU**: Broad partnership framework

### Standard Sections
- Purpose & Scope
- Roles & Responsibilities
- Editorial Control & Standards
- Byline & Credit
- Publication Rights
- Financial Arrangements
- Communication Protocols
- Confidentiality
- Dispute Resolution
- Termination

### Export
- PDF with professional legal formatting
- Signature lines for all parties
- Print-optimized output

## Quick Start

1. Open `index.html` in any modern web browser
2. Select your agreement type
3. Add parties with organization details
4. Review and customize each section
5. Add custom clauses if needed
6. Preview and download the agreement

## Technical Details

### Dependencies (loaded via CDN)
- React 18
- Tailwind CSS
- html2pdf.js
- Google Fonts (Libre Baskerville, Source Sans 3, Source Code Pro)

### Data Persistence
- Agreement drafts saved to browser localStorage
- Organization profiles can be reused
- No server required

### Browser Support
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile responsive with editor/preview toggle

## Customization

### Editing Sections
Each section includes template text with placeholders like `[PARTY 1]`, `[PROJECT NAME]`, etc. Click on a section to expand it and edit the content directly. Party names are automatically replaced in the preview.

### Adding Custom Clauses
Click "Add Custom Clause" to create additional sections not covered by the templates. These appear after the standard sections in the final document.

### Multi-Party Agreements
Click "Add Party" to include additional organizations beyond the initial two. Each party gets their own signature block in the final document.

## Use Cases

- News organizations in collaborative projects
- NJ News Commons members (300+ organizations)
- Journalism collaboratives nationwide
- Content sharing and republishing arrangements
- Joint event organization
- Resource and equipment sharing

## Legal Disclaimer

This tool generates template documents intended as starting points for discussion between collaborating organizations. The generated agreements are not legal advice. Organizations should have their legal counsel review any agreement before signing.

## License

This tool is provided by the Center for Cooperative Media under CC0 1.0 (public domain).

## Author

Created by Joe Amditis for the Center for Cooperative Media.
