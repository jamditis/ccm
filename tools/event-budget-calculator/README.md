# Event Budget Calculator

A comprehensive budget planning tool for events, helping newsrooms and organizations track expenses, revenue, and break-even analysis. Built for the Center for Cooperative Media.

## Features

### Budget Management
- **Expense Categories**: Venue, catering, A/V, marketing, staffing, materials, misc
- **Revenue Sources**: Sponsorships, ticket sales, donations, other revenue
- **Line Items**: Add detailed items with descriptions, amounts, and notes
- **Real-time Calculations**: Instant totals and net income updates

### Financial Analysis
- **Summary Dashboard**: Total revenue, expenses, and net income at a glance
- **Coverage Percentage**: See how much of expenses are covered by revenue
- **Break-even Indicator**: Shows how much more revenue needed to break even

### Data Management
- **Save Budgets**: Store multiple event budgets for reuse
- **Load & Edit**: Retrieve saved budgets and modify as needed
- **Local Storage**: All data persists in browser storage
- **Reset Option**: Clear all data and start fresh

### Export
- **PDF Export**: Professional budget report with summary and line-item detail
- **Print Support**: Optimized print styles

## Quick Start

1. Open `index.html` in any modern web browser
2. Enter event information (name, date, location)
3. Add expense items under each category
4. Add revenue items (sponsorships, tickets, etc.)
5. Review summary for net income and coverage
6. Save budget or export to PDF

## Usage Guide

### Adding Budget Items

1. **Expand a Section**: Click on Expenses or Revenue to expand
2. **Find Category**: Locate the relevant category (e.g., "Catering & Refreshments")
3. **Add Item**: Click "Add Item" button
4. **Enter Details**:
   - Description: What the item is for
   - Amount: Dollar amount
   - Notes: Additional context (optional)
5. **Delete Items**: Hover over item and click trash icon

### Expense Categories

| Category | Examples |
|----------|----------|
| Venue & Space | Room rental, parking, setup fees |
| Catering & Refreshments | Food, beverages, service staff |
| Audio/Visual & Tech | Microphones, projectors, livestreaming |
| Marketing & Promotion | Flyers, social ads, signage |
| Staffing & Speakers | Honoraria, travel, accommodations |
| Materials & Supplies | Name tags, programs, decorations |
| Miscellaneous | Contingency, insurance, permits |

### Revenue Categories

| Category | Examples |
|----------|----------|
| Sponsorships | Presenting, supporting, in-kind sponsors |
| Ticket Sales | Early bird, general admission, VIP |
| Donations & Grants | Foundation grants, individual donations |
| Other Revenue | Merchandise, raffles, partnerships |

### Saving Budgets

1. Click the **Save** button in the header
2. Enter a descriptive name (e.g., "2026 Luncheon - Draft 1")
3. Budget is stored in browser localStorage
4. Load saved budgets from the dropdown menu

### Exporting to PDF

1. Click **Export PDF** button
2. PDF includes:
   - Event name, date, and location
   - Summary with totals
   - Detailed expense breakdown by category
   - Detailed revenue breakdown by category
3. File downloads automatically

## Technical Details

### Dependencies (CDN-loaded)
- React 18 (Production build)
- ReactDOM 18
- Babel (JSX transformation)
- Tailwind CSS
- html2pdf.js (PDF generation)
- Google Fonts (Inter, JetBrains Mono)

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

### Local Storage Keys
- `ccm_event_budgets`: Array of saved budget objects

### Data Structure

```javascript
// Saved Budget Object
{
  id: string,
  name: string,
  eventInfo: {
    name: string,
    date: string,
    location: string,
    description: string
  },
  expenseCategories: [
    {
      id: string,
      name: string,
      items: [
        {
          id: string,
          description: string,
          amount: number,
          notes: string
        }
      ]
    }
  ],
  revenueCategories: [...],
  savedAt: ISO date string
}
```

## File Structure

```
event-budget-calculator/
├── index.html    # Complete single-file application
└── README.md     # This documentation
```

## Customization

### Adding Expense Categories

Edit the `DEFAULT_EXPENSE_CATEGORIES` array:

```javascript
const DEFAULT_EXPENSE_CATEGORIES = [
    { id: 'venue', name: 'Venue & Space', items: [] },
    { id: 'your_category', name: 'Your Category Name', items: [] },
    // ...
];
```

### Adding Revenue Categories

Edit the `DEFAULT_REVENUE_CATEGORIES` array:

```javascript
const DEFAULT_REVENUE_CATEGORIES = [
    { id: 'sponsorships', name: 'Sponsorships', items: [] },
    { id: 'your_source', name: 'Your Revenue Source', items: [] },
    // ...
];
```

### Changing Colors

Modify the Tailwind config to adjust the CCM color palette:

```javascript
colors: {
    ccm: {
        500: '#0ea5e9',  // Primary
        600: '#0284c7',  // Hover
        700: '#0369a1',  // Active
        // ...
    }
}
```

## Tips for Best Results

### For Accurate Budgets
1. Include contingency (10-15% of total expenses)
2. Get multiple quotes for major expenses
3. Track in-kind sponsorships separately
4. Update regularly as plans evolve

### For PDF Export
1. Use Chrome for most consistent results
2. Fill in event name for proper filename
3. Add notes to items for context in exports

### For Team Collaboration
1. Save versions as you iterate (Draft 1, Draft 2, Final)
2. Export PDF to share with stakeholders
3. Note assumptions in the description field

## Troubleshooting

### PDF Not Generating
- Ensure JavaScript is enabled
- Check browser console for errors
- Try a different browser (Chrome recommended)

### Budget Not Saving
- Check if localStorage is enabled
- Don't use private/incognito mode
- Check browser storage limits

### Calculations Incorrect
- Ensure amounts are entered as numbers
- Check for duplicate items
- Verify all items have amounts (not just descriptions)

## Integration with Other CCM Tools

- **Sponsorship Generator**: Create sponsorship tiers, then add expected revenue to this calculator
- **Invoicer**: After event, create invoices for sponsors based on committed amounts

## Credits

- **Created by**: Center for Cooperative Media
- **Organization**: [Center for Cooperative Media](https://centerforcooperativemedia.org/)
- **Year**: 2025

## License

This tool is provided by the Center for Cooperative Media for use in supporting local journalism and media organizations.
