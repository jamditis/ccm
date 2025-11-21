# Sponsorship Package Generator

A professional sponsorship proposal and package generator built for the Center for Cooperative Media. Create customized sponsorship proposals for specific organizations or generate overview sheets showing all available tiers.

## Features

### Two Operating Modes

#### Generator Mode
- Create targeted proposals for specific sponsors
- Customize benefits and pricing per prospect
- Two view options:
  - **Specific Proposal**: Detailed single-tier proposal for one organization
  - **Full Overview**: All sponsorship tiers on one page

#### Builder Mode
- Create and manage sponsorship tiers
- Customize titles, costs, descriptions, and benefits
- Choose from 15+ icons for visual distinction
- Support for both cash and in-kind/trade sponsorships

### Export Options
- **PDF Export**: High-fidelity multi-page PDF with smart page breaks
- **PNG Export**: High-resolution image for digital sharing
- **Print Support**: Optimized print stylesheet

### Data Persistence
- All packages and settings saved to localStorage
- Reset to defaults option available
- Global event information stored separately

## Quick Start

1. Open `index.html` in any modern web browser
2. Configure your event details in the collapsible "Event & Contact Info" panel
3. Select a sponsorship tier or view mode
4. Customize the proposal for your prospect
5. Export as PDF or PNG

## Usage Guide

### Configuring Event Details

Click "Event & Contact Info" to expand the settings panel:

- **Event Title**: Name of your event (e.g., "2026 Community Media Luncheon")
- **Date String**: Formatted date (e.g., "February 19, 2026")
- **Organization Name**: Your organization's name
- **Tagline**: Mission statement or event description
- **Contact Name**: Primary contact person
- **Location**: Office location or city

### Creating a Specific Proposal

1. **Select "Specific Proposal"** from the view toggle
2. **Choose a Tier**: Click on a sponsorship tier from the list
3. **Enter Recipient**: Fill in the organization name you're pitching to
4. **Customize the Offer**:
   - Adjust cost (for cash sponsorships)
   - Modify benefits/deliverables
   - For in-kind: specify trade details and sponsorship item

### Generating an Overview

1. **Select "Full Overview"** from the view toggle
2. All tiers display in a grid format
3. Shows first 3 benefits per tier with "+X more" indicator
4. Perfect for general distribution or initial conversations

### Managing Sponsorship Tiers (Builder Mode)

1. Click **Builder** in the top navigation
2. **Add New Tiers**: Click "Add New" button
3. **Edit Existing**: Click any tier in the left panel
4. **Configure Each Tier**:
   - Package title
   - Cost string (can include text like "Service Exchange")
   - Type (Cash or In-Kind/Trade)
   - Icon selection
   - Description
   - Benefits list (add/remove as needed)
5. **Delete Tiers**: Click trash icon on any tier
6. **Reset**: Use "Reset to Default Packages" to restore defaults

### In-Kind Sponsorships

For trade/in-kind sponsorships:

1. Set tier type to "In-Kind / Trade"
2. In the proposal editor, specify:
   - **They Provide**: What the sponsor will contribute (e.g., "In-language promotion & securing elected official attendance")
   - **We Provide**: What benefit they receive (e.g., "Dessert Station & Coffee Bar")

## Default Sponsorship Tiers

The tool comes pre-configured with six tiers:

| Tier | Cost | Description |
|------|------|-------------|
| Registration Sponsor | $500 | Name tags, pens, welcome signage |
| Advertising Sponsor | $1,000 | Menu cards, signage, program ad |
| Sweet Endings Sponsor | $2,000 | Dessert & coffee service |
| Session Sponsor | $2,500 | Speaking opportunity, stage branding |
| Presenting Sponsor | $5,000 | Premier "Presented By" billing |
| In-Kind Partner | Variable | Custom trade arrangements |

## Technical Details

### Dependencies (CDN-loaded)
- React 18 (Production build)
- ReactDOM 18
- Babel (JSX transformation)
- Tailwind CSS
- html2canvas (Image generation)
- jsPDF (PDF generation)
- Google Fonts (Playfair Display, Space Grotesk, JetBrains Mono)

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

### Local Storage Keys
- `ccm_sponsorship_packages`: Array of sponsorship tier objects
- `ccm_sponsorship_globals`: Event and contact information

## File Structure

```
sponsorship-generator/
├── index.html    # Complete single-file application
└── README.md     # This documentation
```

## Customization

### Adding New Icons

1. Add SVG path to the `Icons` object in the JavaScript
2. Add icon name to `AVAILABLE_ICONS` array
3. Icon will appear in Builder mode icon selector

### Modifying Default Packages

Edit the `DEFAULT_PACKAGES` array:

```javascript
const DEFAULT_PACKAGES = [
    {
        id: 'my_tier',
        title: 'Custom Tier Name',
        cost: '$750',
        type: 'cash',  // or 'trade'
        iconName: 'Award',
        description: 'Your value proposition here.',
        benefits: [
            'Benefit one',
            'Benefit two'
        ]
    },
    // ... more tiers
];
```

### Changing Event Defaults

Edit the `DEFAULT_GLOBALS` object:

```javascript
const DEFAULT_GLOBALS = {
    eventName: 'Your Event Name',
    eventDate: 'Month Day, Year',
    orgName: 'Your Organization',
    tagline: 'Your mission statement.',
    contactName: 'Contact Person',
    contactLocation: 'City, State'
};
```

### Styling the Document

- **CMYK Border**: Modify the decorative top border colors
- **Fonts**: Update the `FONTS` object to change typography
- **Colors**: Modify Tailwind classes throughout the template

## PDF Export Details

The PDF export system:
- Uses html2canvas to render the document
- Applies smart page break detection to avoid splitting elements
- Respects `.break-inside-avoid` classes
- Produces letter-size (8.5" x 11") pages
- Maintains background colors and styling

## Tips for Best Results

### For Proposals
1. Keep benefit descriptions concise
2. Customize the value proposition for each prospect
3. Match sponsorship items to sponsor interests

### For Exports
1. Use Chrome for most consistent PDF output
2. Allow time for canvas rendering on complex documents
3. Check preview before exporting

### For Events
1. Create tier pricing that makes sense as a progression
2. Clearly differentiate benefits between tiers
3. Include unique/exclusive benefits at higher tiers

## Troubleshooting

### PDF Export Issues
- Ensure pop-up blockers don't interfere
- Check browser console for JavaScript errors
- Try PNG export as alternative

### Changes Not Saving
- Verify localStorage is enabled
- Don't use private/incognito mode
- Check browser storage limits

### Layout Problems
- Ensure stable internet for CDN dependencies
- Clear cache and reload
- Check for JavaScript errors

### Print Issues
- Use "Save as PDF" from print dialog
- Disable "Headers and Footers" option
- Set margins to minimum

## API Reference

### Package Object Structure

```javascript
{
    id: string,           // Unique identifier
    title: string,        // Display name
    cost: string,         // Cost string (e.g., "$1,000")
    type: 'cash' | 'trade',
    iconName: string,     // Icon component name
    description: string,  // Value proposition
    benefits: string[]    // Array of benefit strings
}
```

### Global Settings Structure

```javascript
{
    eventName: string,
    eventDate: string,
    orgName: string,
    tagline: string,
    contactName: string,
    contactLocation: string
}
```

## Credits

- **Organization**: [Center for Cooperative Media](https://centerforcooperativemedia.org/)
- **Version**: 2.5 (Stable)

## License

This tool is provided by the Center for Cooperative Media for use in supporting local journalism and media organizations.
