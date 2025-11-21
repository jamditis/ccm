# Invoicer

A modern, professional invoice generator built for the Center for Cooperative Media. Create beautiful, customizable invoices and export them as PDFs with a sleek, studio-quality design.

## Features

### Invoice Creation
- **Professional Templates**: Clean, modern invoice design with customizable aesthetics
- **Line Items**: Add multiple services/products with descriptions, dates, rates, and quantities
- **Auto-Calculation**: Automatic subtotal and total calculations
- **Logo Support**: Upload your organization's logo for branded invoices

### Customization Options
- **Accent Colors**: Choose any color for the invoice header
- **Typography Styles**:
  - Modern Geometric (Plus Jakarta Sans)
  - Editorial Serif (Cormorant Garamond)
  - Technical Mono (IBM Plex Mono)
- **Corner Styles**: Sharp, Subtle, Soft, or Round corners
- **Smart Contrast**: Text automatically adjusts for readability on any background color

### Data Management
- **Save Profiles**: Store sender information, notes, and theme preferences for quick reuse
- **Load Profiles**: Instantly populate forms with saved profile data
- **Local Storage**: All profiles persist in browser storage

### Export
- **PDF Download**: High-quality PDF export with preserved styling
- **Print Support**: Optimized print styles for direct printing

## Quick Start

1. Open `index.html` in any modern web browser
2. Fill in your sender information (name, address, email, phone)
3. Add recipient/client details
4. Add line items for your services
5. Customize the design using the Aesthetics panel
6. Click "Download PDF" to export

## Usage Guide

### Setting Up Your Profile

1. **Sender Information**: Enter your name, title, address, email, phone, and payment instructions
2. **Save Profile**: Click the save icon and name your profile (e.g., "My Consulting Business")
3. **Reuse Later**: Select your profile from the dropdown to auto-fill sender details

### Creating an Invoice

1. **Invoice Details**:
   - Set invoice number (e.g., INV-2025-001)
   - Upload your logo (optional)
   - Set issue and due dates

2. **Bill To**:
   - Enter client company name
   - Add attention to field
   - Include client address

3. **Line Items**:
   - Click "Add Item" for each service
   - Fill in description, date, rate, and quantity
   - Remove items with the trash icon (hover to reveal)

4. **Footer Note**: Add thank you message or terms

### Customizing Design

- **Accent Color**: Click the color picker to choose your header color
- **Corners**: Select corner radius (Sharp to Round)
- **Typography**: Choose font style that matches your brand

### Payment Instructions

Include your payment details in the "Payment Instructions" field:
- Bank name and account details
- Zelle/Venmo information
- Check mailing address
- Payment terms

## Technical Details

### Dependencies (CDN-loaded)
- React 18
- ReactDOM 18
- Babel (for JSX transformation)
- Tailwind CSS
- html2pdf.js (PDF generation)
- Lucide Icons
- Google Fonts (Syne, Plus Jakarta Sans, Cormorant Garamond, IBM Plex Mono)

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

### Local Storage
The application uses browser localStorage to persist:
- Saved profiles (sender info, notes, themes)

## File Structure

```
invoicer/
├── index.html    # Complete single-file application
└── README.md     # This documentation
```

## Customization

### Modifying Default Values

Edit the `useState` hooks in the `InvoiceTool` component to change defaults:

```javascript
const [meta, setMeta] = useState({
    number: 'INV-2025-001',  // Default invoice number
    dateIssued: new Date().toISOString().split('T')[0],
    dateDue: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    logo: null
});
```

### Adding Custom Fonts

1. Add font import in the `<head>` section
2. Update Tailwind config to include the new font family
3. Add option to typography selector

### Changing Color Themes

Modify the `tailwind.config` object to add new color palettes:

```javascript
colors: {
    studio: {
        900: '#0f0c29',
        // Add more colors...
    }
}
```

## Tips for Best Results

1. **Logo Images**: Use PNG with transparent background for best results
2. **PDF Export**: For consistent results, use Chrome browser
3. **Long Descriptions**: Keep line item descriptions concise for better table layout
4. **Payment Info**: Format as multiple lines for readability

## Troubleshooting

### PDF Not Generating
- Ensure JavaScript is enabled
- Check browser console for errors
- Try a different browser

### Styling Issues
- Clear browser cache
- Check internet connection (CDN dependencies)
- Ensure pop-up blockers aren't interfering

### Profile Not Saving
- Check if localStorage is enabled
- Ensure browser isn't in private/incognito mode

## Credits

- **Created by**: [Joe Amditis](https://twitter.com/jsamditis)
- **Organization**: [Center for Cooperative Media](https://centerforcooperativemedia.org/)
- **Year**: 2025

## License

This tool is provided by the Center for Cooperative Media for use in supporting local journalism and media organizations.
