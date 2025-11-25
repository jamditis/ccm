# Sponsorship Package Generator

A professional sponsorship proposal and package generator built for the Center for Cooperative Media. Create customized sponsorship proposals for specific organizations or generate overview sheets showing all available tiers.

## Features

### Two Operating Modes

#### Generator Mode
- Create targeted proposals for specific sponsors
- Customize benefits and pricing per prospect
- **Drag-and-drop** package reordering
- Two view options:
  - **Specific Proposal**: Detailed single-tier proposal for one organization
  - **Full Overview**: All sponsorship tiers on one page (shows all benefits)

#### Builder Mode
- Create and manage sponsorship tiers
- Customize titles, costs, descriptions, and benefits
- Choose from 20+ icons for visual distinction
- Support for both cash and in-kind/trade sponsorships

### Branding & Customization
- **Logo Upload**: Add your organization's logo to proposals
- **Header Color Bars**: Customize the four-color decorative header
- **Editable Footer Labels**: Change "Contact" and "Office" labels to anything

### Sharing & Templates
- **Share Link**: Generate a URL that encodes the entire configuration
- **Templates**: Save configurations as reusable templates
- **URL-based Loading**: Open shared links in a new browser tab to continue editing

### Export Options
- **PDF Export**: High-fidelity multi-page PDF with smart page breaks
- **PNG Export**: High-resolution image for digital sharing
- **Print Support**: Optimized print stylesheet

### Data Persistence
- All packages and settings saved to localStorage
- Templates saved separately for reuse
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

- **Event Logo**: Upload your organization's logo (appears in header and footer)
- **Event Title**: Name of your event (e.g., "2026 Community Media Luncheon")
- **Date String**: Formatted date (e.g., "February 19, 2026")
- **Organization Name**: Your organization's name
- **Tagline**: Mission statement or event description
- **Footer Label 1 & Value**: Customizable contact field (default: "Contact")
- **Footer Label 2 & Value**: Customizable location field (default: "Office")
- **Header Bar Colors**: Four color pickers to customize the decorative header

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
3. Shows all benefits for each tier (no truncation)
4. Perfect for general distribution or initial conversations

### Reordering Packages

- In Generator Mode, drag packages using the grip handle to reorder them
- The new order is saved automatically and persists across sessions
- Order changes apply to both Specific Proposal and Full Overview modes

### Sharing & Templates

#### Share Link
1. Click the **Share** button in the navbar
2. A URL containing your configuration is copied to clipboard
3. Share this URL with others - they can open it to see and edit your configuration

#### Using Templates
1. Click the **Templates** button in the navbar
2. **Save Template**: Enter a name and click Save to store current configuration
3. **Load Template**: Click Load on any saved template to restore it
4. **Delete Template**: Click the trash icon to remove a template

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
- `ccm_sponsorship_templates`: Array of saved template configurations

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
    contactLocation: string,
    contactLabel: string,      // Customizable footer label (default: "Contact")
    locationLabel: string,     // Customizable footer label (default: "Office")
    logo: string | null,       // Base64-encoded logo image
    headerColors: string[]     // Array of 4 hex color codes for header bars
}
```

## Changelog

### v2.6
- Added drag-and-drop reordering for packages in Generator Mode
- Added logo upload functionality (displays in header and footer)
- Added customizable header color bars (4-color picker)
- Added editable footer labels (rename "Contact" and "Office")
- Removed benefit truncation in Full Overview mode (shows all benefits)
- Added shareable URL links for configuration sharing
- Added template save/load functionality
- UI improvements for responsive navbar

### v2.5
- Initial stable release with Generator and Builder modes
- PDF and PNG export with smart page breaks
- localStorage persistence

## Credits

- **Organization**: [Center for Cooperative Media](https://centerforcooperativemedia.org/)
- **Version**: 2.6

## License

This tool is provided by the Center for Cooperative Media for use in supporting local journalism and media organizations.
