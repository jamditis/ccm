# Tool PRDs & Build Plans

Product Requirements Documents for upcoming CCM tools.

---

## 1. Media Kit Builder

### Overview
A tool for newsrooms to create professional media kits/press kits to share with advertisers, sponsors, and partners. Presents audience data, ad rates, and platform information in a polished, brandable format.

### Target Users
- Small/local newsrooms seeking advertisers
- Independent publishers
- News organizations professionalizing ad sales
- Freelancers with established audiences

### Key Features

#### Core Functionality
- **Organization Profile**: Name, logo, mission statement, founding year
- **Audience Demographics**: Age, location, income, education, interests
- **Reach Metrics**: Monthly visitors, subscribers, social followers, email list size
- **Platform Breakdown**: Print, web, newsletter, social media, podcast
- **Ad Rate Cards**: Display, sponsored content, newsletter, social
- **Ad Specifications**: Sizes, formats, deadlines, file requirements

#### Customization
- Brandable colors and fonts (consistent with other CCM tools)
- Logo upload
- Multiple rate card templates (standard, premium, nonprofit)
- Show/hide sections based on platforms offered

#### Export
- PDF export (primary)
- PNG for social/email sharing
- Print-optimized styles

### Technical Approach

**Architecture**: Single-file HTML (like Invoicer and Sponsorship Generator)

**Dependencies** (CDN):
- React 18
- Tailwind CSS
- html2pdf.js
- Google Fonts

**Data Structure**:
```javascript
{
  organization: {
    name: string,
    logo: base64,
    tagline: string,
    foundedYear: number,
    website: string,
    contact: { name, email, phone }
  },
  audience: {
    totalReach: number,
    demographics: {
      ageRanges: [{ range: string, percentage: number }],
      locations: [{ area: string, percentage: number }],
      interests: string[]
    }
  },
  platforms: [
    {
      name: string, // "Website", "Newsletter", etc.
      metrics: { label: string, value: string }[],
      adOptions: [
        {
          name: string,
          description: string,
          rate: string,
          specs: string
        }
      ]
    }
  ],
  testimonials: [{ quote: string, source: string }]
}
```

**Local Storage**: Save/load media kit profiles

### UI/UX

**Editor Panel** (left side):
- Collapsible sections for each data category
- Drag-and-drop platform reordering
- Real-time preview updates

**Preview Panel** (right side):
- Live document preview
- Page break indicators
- Zoom controls

**Design Notes**:
- Professional, clean aesthetic
- Data visualization for demographics (simple bar charts)
- Consistent with CCM tool family styling

### Build Phases

1. **Phase 1**: Core structure and organization info
2. **Phase 2**: Audience demographics with visualizations
3. **Phase 3**: Platform sections and ad rate cards
4. **Phase 4**: Export functionality and profile saving

### Success Metrics
- User can create complete media kit in <15 minutes
- PDF output is presentation-ready
- Profiles persist across sessions

---

## 2. Freelancer Rate Calculator

### Overview
A calculator to help freelance journalists determine fair rates based on project type, complexity, rights, turnaround, and market benchmarks. Outputs professional rate quotes.

### Target Users
- Freelance journalists
- Independent writers and photographers
- Newsroom editors budgeting for freelancers
- Journalism students entering the workforce

### Key Features

#### Core Functionality
- **Project Type Selection**: Article, photo essay, video, podcast, social content, editing
- **Rate Calculation Methods**: Per word, per hour, per project, day rate
- **Complexity Factors**: Research depth, travel, specialized expertise, rush fee
- **Rights & Licensing**: FNASR, work-for-hire, exclusive, reprint rights
- **Market Benchmarks**: Reference rates from industry surveys

#### Calculations
- Base rate calculation
- Complexity multipliers
- Rush fee additions (24hr, 48hr, 1 week)
- Rights premiums
- Kill fee recommendations (25-50% of total)
- Expense estimates

#### Output
- Rate breakdown summary
- Professional quote template
- Integration with Invoicer (export line items)

### Technical Approach

**Architecture**: Single-file HTML

**Dependencies** (CDN):
- React 18
- Tailwind CSS
- Optional: Chart.js for rate comparisons

**Data Structure**:
```javascript
{
  projectType: string,
  rateMethod: 'word' | 'hour' | 'project' | 'day',
  baseMetrics: {
    wordCount: number,
    hours: number,
    // etc.
  },
  complexity: {
    research: 'light' | 'moderate' | 'deep',
    travel: boolean,
    specialized: boolean,
    interviews: number
  },
  turnaround: 'standard' | 'rush_week' | 'rush_48h' | 'rush_24h',
  rights: 'fnasr' | 'exclusive_limited' | 'exclusive_perpetual' | 'work_for_hire',
  expenses: [{ item: string, cost: number }]
}

// Market benchmarks (embedded data)
const BENCHMARKS = {
  article: {
    low: 0.25,    // per word
    median: 0.50,
    high: 1.00
  },
  // ...
}
```

**Local Storage**: Save rate profiles, custom benchmarks

### UI/UX

**Calculator Flow**:
1. Select project type
2. Enter base metrics (words, hours, etc.)
3. Adjust complexity factors
4. Set turnaround and rights
5. Add expenses
6. View calculated rate with breakdown

**Output Display**:
- Total rate prominently displayed
- Breakdown of each component
- Market comparison indicator
- Copy-friendly quote text

**Design Notes**:
- Step-by-step wizard or single-page with sections
- Real-time calculation updates
- Visual indicators for rate positioning vs. market

### Build Phases

1. **Phase 1**: Basic rate calculation (word/hour)
2. **Phase 2**: Complexity and rights multipliers
3. **Phase 3**: Market benchmarks and comparisons
4. **Phase 4**: Quote generation and export

### Success Metrics
- Accurate calculations matching industry standards
- Clear breakdown helps users justify rates
- Quote export is professional and ready-to-send

---

## 3. Grant Proposal Outline Generator

### Overview
A tool to structure grant proposals with sections aligned to common journalism funder requirements. Helps newsrooms organize their thinking and ensure they address all required elements.

### Target Users
- Local newsrooms seeking funding
- News startups
- Journalism nonprofits
- Independent projects seeking support
- CCM itself and collaborative journalism projects

### Key Features

#### Core Functionality
- **Funder Templates**: Pre-built structures for common funders
  - Knight Foundation
  - Google News Initiative
  - Report for America
  - Local Media Association
  - Generic journalism grant
- **Proposal Modes**: Letter of Inquiry (LOI) vs. Full Proposal
- **Section Builder**: Standard grant sections with guidance
- **Attachment Checklist**: Track required documents

#### Sections (Full Proposal)
1. Executive Summary
2. Organization Background
3. Problem Statement / Need
4. Project Description
5. Goals & Objectives
6. Methods / Activities
7. Timeline / Milestones
8. Evaluation Plan
9. Budget & Justification
10. Sustainability Plan
11. Key Personnel

#### Guidance Features
- Section-by-section writing prompts
- Character/word count limits per funder
- Example snippets (anonymized)
- Common pitfalls to avoid

#### Export
- PDF outline with all sections
- Copy individual sections
- Checklist export

### Technical Approach

**Architecture**: Single-file HTML

**Dependencies** (CDN):
- React 18
- Tailwind CSS
- html2pdf.js

**Data Structure**:
```javascript
{
  funderTemplate: string,
  proposalType: 'loi' | 'full',
  projectInfo: {
    title: string,
    requestAmount: number,
    duration: string,
    organization: string
  },
  sections: [
    {
      id: string,
      title: string,
      content: string,
      guidance: string,
      maxLength: number,
      required: boolean,
      complete: boolean
    }
  ],
  attachments: [
    {
      name: string,
      required: boolean,
      uploaded: boolean,
      notes: string
    }
  ]
}

// Funder templates (embedded)
const TEMPLATES = {
  knight: {
    name: 'Knight Foundation',
    sections: [...],
    attachments: [...],
    tips: string
  },
  // ...
}
```

**Local Storage**: Save proposal drafts, organization info

### UI/UX

**Layout**:
- Funder/mode selector at top
- Section navigation sidebar
- Main content area with current section
- Progress indicator

**Editor Features**:
- Rich text or markdown support
- Word/character counter with limit warnings
- Expandable guidance panels
- Section completion checkmarks

**Design Notes**:
- Clean, focused writing environment
- Non-distracting interface
- Clear visual progress tracking

### Build Phases

1. **Phase 1**: Basic section structure and navigation
2. **Phase 2**: Funder templates with guidance
3. **Phase 3**: Progress tracking and validation
4. **Phase 4**: Export and draft saving

### Success Metrics
- Users complete proposals faster with structure
- All required sections addressed
- Guidance reduces common errors

---

## 4. Collaboration Agreement Generator

### Overview
Create MOUs (Memoranda of Understanding) or collaboration agreements between news organizations for joint reporting projects, shared resources, or republishing arrangements.

### Target Users
- News organizations in collaborative projects
- NJ News Commons members (300+ organizations)
- Journalism collaboratives nationwide
- CCM for its own partnership work

### Key Features

#### Core Functionality
- **Agreement Types**:
  - Shared Reporting (joint investigation/project)
  - Republishing/Content Sharing
  - Resource Sharing (staff, equipment, data)
  - Event Co-hosting
  - General Partnership MOU
- **Multi-Party Support**: 2+ organizations
- **Section Builder**: Standard legal/agreement sections

#### Agreement Sections
1. Parties (all participating organizations)
2. Purpose & Scope
3. Duration / Timeline
4. Roles & Responsibilities
5. Editorial Control & Standards
6. Byline & Credit
7. Publication Rights
8. Financial Arrangements (if any)
9. Communication Protocols
10. Confidentiality
11. Dispute Resolution
12. Termination
13. Signatures

#### Customization
- Add/remove/reorder sections
- Custom clauses
- Organization branding (logo on final doc)
- Multiple signature lines

#### Export
- PDF with signature lines
- Word-compatible format (if feasible)
- Print-optimized

### Technical Approach

**Architecture**: Single-file HTML

**Dependencies** (CDN):
- React 18
- Tailwind CSS
- html2pdf.js or jsPDF

**Data Structure**:
```javascript
{
  agreementType: string,
  title: string,
  effectiveDate: string,
  parties: [
    {
      id: string,
      orgName: string,
      contactName: string,
      contactTitle: string,
      contactEmail: string,
      address: string,
      role: string  // "Lead", "Partner", etc.
    }
  ],
  sections: [
    {
      id: string,
      title: string,
      content: string,
      editable: boolean,
      included: boolean
    }
  ],
  customClauses: [
    {
      title: string,
      content: string
    }
  ]
}

// Agreement templates (embedded)
const TEMPLATES = {
  shared_reporting: {
    name: 'Shared Reporting Project',
    description: 'For joint investigations...',
    sections: [...],
    boilerplate: {...}
  },
  // ...
}
```

**Local Storage**: Save agreement drafts, organization profiles

### UI/UX

**Layout**:
- Agreement type selector
- Party manager (add/edit organizations)
- Section editor with live preview
- Signature block preview

**Editor Features**:
- Template-based starting content
- Inline editing of boilerplate
- Party name auto-population in text
- Section reordering

**Design Notes**:
- Professional, legal-document aesthetic
- Clear distinction between template and custom text
- Preview closely matches final PDF

### Build Phases

1. **Phase 1**: Basic agreement structure and party management
2. **Phase 2**: Agreement type templates
3. **Phase 3**: Section editing and customization
4. **Phase 4**: Export with signatures and draft saving

### Success Metrics
- Agreements are legally sound starting points
- Users can customize without legal expertise
- Export is professional and signable

---

## Implementation Priority

Recommended build order based on complexity and user value:

1. **Freelancer Rate Calculator** - Simpler logic, high immediate value
2. **Media Kit Builder** - Moderate complexity, complements sponsorship tool
3. **Collaboration Agreement Generator** - Aligns with CCM mission
4. **Grant Proposal Outline Generator** - Most complex, highest value for newsrooms

---

## Shared Technical Patterns

All tools should follow these patterns for consistency:

### Code Structure
- Single-file HTML (CDN dependencies)
- React functional components with hooks
- Tailwind CSS for styling
- Local storage for persistence

### UI Patterns
- Collapsible configuration panels
- Live preview
- Profile save/load
- PDF export
- Consistent color scheme and fonts

### Documentation
- README.md with features, usage guide, technical details
- Inline JSDoc comments for complex functions
