# Media Kit Builder

A tool for newsrooms to create professional media kits/press kits to share with advertisers, sponsors, and partners. Presents audience data, ad rates, and platform information in a polished, brandable format.

## Features

### Core Functionality
- **Organization Profile**: Name, logo, tagline, mission statement, founding year
- **Audience Demographics**: Age, gender, income distribution, geographic locations, interests
- **Reach Metrics**: Total audience reach displayed prominently
- **Platform Breakdown**: Website, Newsletter, Social Media, Podcast, Print, Events
- **Ad Rate Cards**: Customizable ad options with pricing and specs
- **Package Bundles**: Combined ad offerings across platforms
- **Case Studies**: Success stories from past advertisers
- **Testimonials**: Quotes from partners and advertisers

### Data Management
- **Auto-save**: Changes saved automatically every 30 seconds
- **Profile Management**: Save, load, and delete multiple media kit profiles
- **Export/Import**: JSON export for backup and sharing between browsers
- **Form Validation**: Warnings when demographic percentages don't sum to 100%
- **Toast Notifications**: Visual feedback for save, delete, and export actions

### Customization
- Custom primary and accent colors
- Logo upload
- Enable/disable platforms based on your offerings
- Add multiple ad options per platform
- Real-time preview updates

### Export
- **PDF Export**: Professional formatting with print-optimized styles
- **PNG Export**: High-resolution image of your media kit
- Clean, presentation-ready output

## Quick Start

1. Open `index.html` in any modern web browser
2. Set your brand colors in Theme & Branding
3. Fill in your organization profile
4. Add audience demographics (age, gender, income, geography, interests)
5. Enable relevant platforms and set ad rates
6. Create package bundles for combined offerings
7. Add case studies and testimonials
8. Preview and download your media kit (PDF or PNG)

## Technical Details

### Dependencies (loaded via CDN)
- React 18
- Tailwind CSS
- html2pdf.js
- html2canvas
- Google Fonts (Fraunces, Outfit, JetBrains Mono)

### Data Persistence
- Media kit profiles saved to browser localStorage
- Auto-save every 30 seconds
- Export/import JSON for portability
- No server required - works entirely offline

### Browser Support
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile responsive design with editor/preview toggle

## Sections

### Organization Profile
- Organization name and logo
- Tagline/slogan
- Mission statement
- Founded year
- Website URL
- Contact person details

### Audience Demographics
- Total audience reach (combined across platforms)
- Age distribution with visual bar charts
- Gender distribution (Female, Male, Other)
- Income distribution (Under $50K, $50K-$100K, $100K-$150K, $150K+)
- Geographic distribution by region/city
- Audience interests tags

### Platforms

Each platform includes:
- Enable/disable toggle
- Key metrics (varies by platform)
- Ad options with name, description, and rate

**Available Platforms:**
- Website (visitors, page views, time on site)
- Newsletter (subscribers, open rate, click rate)
- Social Media (followers, engagement rate)
- Podcast (downloads per episode, total episodes)
- Print (circulation, distribution points, frequency)
- Events (annual events, total attendance, avg attendance per event)

### Package Bundles
- Combine ad options from multiple platforms
- Set package pricing (often at a discount)
- Describe value proposition
- Toggle packages on/off

### Case Studies
- Advertiser/partner name
- Campaign type and dates
- Results achieved
- Quote from the client

### Testimonials
- Quotes from advertisers/partners
- Source attribution
- Multiple testimonials supported

## Use Cases

- Small/local newsrooms seeking advertisers
- Independent publishers pitching sponsors
- News organizations professionalizing ad sales
- Freelancers with established audiences
- Grant applications requiring audience data

## Tips for Effective Media Kits

1. **Be Specific**: Use actual metrics, not estimates
2. **Show Value**: Highlight engagement rates, not just raw numbers
3. **Include Proof**: Case studies and testimonials build credibility
4. **Bundle Wisely**: Package deals can increase ad spend
5. **Update Regularly**: Keep metrics current

## License

This tool is provided by the Center for Cooperative Media under CC0 1.0 (public domain).

## Author

Created by Joe Amditis for the Center for Cooperative Media.
