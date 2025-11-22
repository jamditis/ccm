# Event budget ledger
A comprehensive budget planning tool designed with a classic ledger aesthetic, helping newsrooms and organizations track expenses, revenue, and break-even analysis. Built for the Center for cooperative media.

## Features

### Budget management
-   **Tabbed interface**: Clean separation between expenses and revenue for focused data entry
-   **Expense categories**: Venue, catering, A/V, marketing, staffing, materials, misc
-   **Revenue sources**: Sponsorships, ticket sales, donations, other revenue
-   **Line items**: Add detailed items with descriptions, amounts, and notes
-   **Real-time calculations**: Instant totals and net income updates

### Financial analysis
-   **Floating ledger widget**: A sticky dashboard tracking net balance, progress bars, and coverage percentage that follows you as you scroll
-   **Visual indicators**: Color-coded metrics (Green for revenue/profit, Red for expenses/loss)
-   **Coverage tracking**: Automatically calculates how much of your budget is covered by revenue
    
### User experience
-   **Toast notifications**: Non-intrusive status updates for saving, loading, and errors
-   **Ledger aesthetic**: Custom "paper" textures, noise overlays, and serif typography for a tactile feel
-   **Responsive inputs**: Styled form elements with currency prefixes and focus states
    

### Data management
-   **Save budgets**: Store multiple event budgets in local browser storage
-   **Load & edit**: Retrieve saved budgets via a dropdown menu
-   **Reset option**: Clear all data and start fresh
    

### Export
-   **PDF export**: Generates a clean, high-contrast, ink-friendly print view separate from the web interface
-   **Print optimization**: Removes UI elements and textures for professional reporting
    

## Quick start
1.  Open `event_budget_ledger.html` in any modern web browser
2.  Enter event information (name, date, location) in the top section
3.  Switch between **Expenses** and **Revenue** tabs using the toggle
4.  Add items under each category
5.  Review the floating summary widget for net income status
6.  Save budget or export to PDF

## Usage guide

### Adding budget items
1.  **Select tab**: Click "Expenses" or "Revenue" to view the relevant ledger
2.  **Expand a section**: Click on a category header (e.g., "Catering & refreshments") to reveal items
3.  **Add item**: Click the "Add entry" button at the bottom of the category
4.  **Enter details**:
    -   Description: What the item is for
    -   Amount: Dollar amount
    -   Notes: Additional context (optional)

5.  **Delete items**: Hover over an item row and click the trash icon that appears

### Expense categories
Category
Examples
Venue & space
Room rental, parking, setup fees
Catering & refreshments
Food, beverages, service staff
Audio/visual & tech
Microphones, projectors, livestreaming
Marketing & promotion
Flyers, social ads, signage
Staffing & speakers
Honoraria, travel, accommodations
Materials & supplies
Name tags, programs, decorations
Miscellaneous
Contingency, insurance, permits

### Revenue categories
Category
Examples
Sponsorships
Presenting, supporting, in-kind sponsors
Ticket sales
Early bird, general admission, VIP
Donations & grants
Foundation grants, individual donations
Other revenue
Merchandise, raffles, partnerships

### Saving budgets
1.  Click the **Save** button in the top navigation bar
2.  Ensure you have entered an "Event name" first
3.  A toast notification will confirm the save
4.  Load previously saved budgets from the "Load saved" dropdown menu

### Exporting to PDF
1.  Click the **Export PDF** button in the navigation bar
2.  The tool generates a specific print-layout view (hidden on screen)
3.  PDF includes:
    -   Event name, date, and location
    -   Executive summary with high-level totals
    -   Detailed tables for revenue and expenses  
    -   Footer with generation date

## Technical details

### Dependencies (CDN-loaded)
-   React 18 (Production build)
-   ReactDOM 18
-   Babel (JSX transformation)
-   Tailwind CSS
-   html2pdf.js (PDF generation)
-   Google Fonts (Libre Baskerville, Manrope, JetBrains Mono)
    
### Browser compatibility
-   Chrome (recommended for best PDF generation)
-   Firefox
-   Safari 
-   Edge

### Local storage keys
-   `ccm_ledger_data`: Array of saved budget objects

### Data structure
    // Saved Budget Object
    {
      id: string,
      name: string,
      updatedAt: ISO date string,
      data: {
        eventInfo: { ... },
        expenseCategories: [ ... ],
        revenueCategories: [ ... ]
      }
    }
    
## File structure
    event-budget-calculator/
    ├── event_budget_ledger.html    # Complete single-file application
    └── README.md                   # This documentation
    
## Customization

### Changing the color palette
This tool uses a semantic color system defined in the `tailwind.config` script within the HTML. To change the theme, locate the `colors` object:

    colors: {
        paper: '#fdfbf7',       // Background color
        ink: {
            50: '#f4f6f8',      // Lightest gray
            // ...
            900: '#1f2933',     // Darkest (text)
        },
        ledger: {
            green: '#059669',   // Revenue/Profit
            red: '#e11d48',     // Expense/Loss
            gold: '#d97706',    // Accents
            accent: '#3b82f6'   // Focus rings
        }
    }  

### Modifying categories
You can edit the `DEFAULT_EXPENSE_CATEGORIES` or `DEFAULT_REVENUE_CATEGORIES` arrays in the JavaScript section to change the default template for new budgets.

## Tips for best results

### For accurate budgets
1.  Include contingency (10-15% of total expenses) in the "Miscellaneous" category
2.  Use the note fields to track quote sources 
3.  Check the "Coverage" percentage in the floating widget to gauge financial health
    
### For PDF export
1.  Use Chrome for the most consistent rendering of the print layout
2.  Fill in the event description, as this appears in the "Overview" section of the PDF
    
## Troubleshooting

### PDF not generating
-   Ensure JavaScript is enabled   
-   Check browser console for errors   
-   If using Safari, try Chrome (html2pdf.js works best in Blink-based browsers)   

### Budget not saving
-   Check if localStorage is enabled in your browser settings 
-   Ensure you are not in Incognito/Private mode, which clears storage on close
    
## Integration with other CCM tools
-   **Sponsorship generator**: Create sponsorship tiers, then add expected revenue to this ledger   
-   **Invoicer**: Use the final PDF report to generate invoice data for sponsors
    
## Credits
-   **Created by**: Center for cooperative media
-   **Organization**: [Center for cooperative media](https://centerforcooperativemedia.org/ "null")
-   **Year**: 2025  

## License
This tool is provided by the Center for cooperative media for use in supporting local journalism and media organizations.
