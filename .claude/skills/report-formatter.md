# Report Formatting Skill

This skill defines the professional formatting standards for Center for Cooperative Media (CCM) reports. Use these conventions when converting research into polished, publication-ready reports.

---

## Document Structure Standards

### Front Matter (Required)
Every report must begin with:
1. **Title** - Use single # heading
2. **Subtitle** (if applicable) - Use ### heading
3. **Metadata block** - Include relevant context
4. **Horizontal separator** - Use `---`

```markdown
# Report Title
## Optional Subtitle

**Prepared for:** Organization Name
**Prepared by:** Author/Team
**Analysis Date:** Month Day, Year
**Report Generated:** Month Day, Year

---
```

### Core Sections (Standard Order)
1. Executive Summary
2. Key Findings (bullet points)
3. Main Content (organized by theme/priority)
4. Methodology (if applicable)
5. Conclusions/Recommendations
6. Next Steps/Action Items
7. Appendices/References

### Section Separators
- Use `---` horizontal rules between major sections
- Use one blank line between paragraphs
- Use two blank lines before major heading transitions

---

## Table Formatting Standards

### Basic Table Structure
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

### Column Alignment
Use colons in separator row to control alignment:
```markdown
| Left Aligned | Centered | Right Aligned |
|:-------------|:--------:|-------------:|
| Text         | Text     | $1,000       |
```

**Standard alignments:**
- Text columns: Left align (`:----`)
- Numbers/Currency: Right align (`----:`)
- Status/Category: Center align (`:----:`)
- Mixed content: Left align (default)

### Table Types

#### Contact Tables
```markdown
| Name | Title | Contact |
|------|-------|---------|
| Jane Doe | Director | jane@example.com |
| John Smith | Manager | (555) 123-4567 |
```

#### Budget Tables
```markdown
| EXPENSE ITEM | AMOUNT |
| :---- | ----: |
| Salaries and benefits | $80,000 |
| Technology costs | $5,000 |
| Travel expenses | $6,000 |
| **TOTAL** | **$91,000** |
```

**Budget conventions:**
- Use ALL CAPS for "EXPENSE ITEM" and "AMOUNT" headers
- Left-align expense descriptions
- Right-align dollar amounts
- Bold the TOTAL row
- Include dollar signs with amounts
- Use comma separators for thousands

#### Ranking/Scoring Tables
```markdown
| Rank | Story | Outlet | Reporter | Score | Category |
|------|-------|--------|----------|-------|----------|
| 1 | Story Title | Outlet Name | Reporter Name | 10/10 | Category |
| 2 | Story Title | Outlet Name | Reporter Name | 9.5/10 | Category |
```

#### Priority Matrix Tables
```markdown
| Priority | Organization | Status | Fit | Recommended Tier | Action Required |
|----------|-------------|--------|-----|------------------|-----------------|
| 🔴 HIGH | Org Name | Active | ⭐⭐⭐⭐⭐ | Top Tier | Contact this week |
| 🟡 MED | Org Name | Pending | ⭐⭐⭐ | Mid Tier | Follow up next month |
```

**Priority indicators:**
- 🔴 HIGH / ⭐⭐⭐⭐⭐ EXCELLENT
- 🟡 MED / ⭐⭐⭐ MEDIUM
- 🟠 LOW / ⭐⭐ LOW
- ⚫ SKIP / ⚪ N/A

#### Comparison Tables
```markdown
| Feature | Option A | Option B | Recommendation |
|---------|----------|----------|----------------|
| Cost | $500 | $750 | Option A |
| Timeline | 2 weeks | 1 week | Option B |
| Quality | Good | Excellent | Option B |
```

---

## Section Writing Standards

### Executive Summary
**Purpose:** Standalone summary that busy readers can understand without reading full report.

**Structure:**
- 2-5 paragraphs maximum
- Lead with the main finding or recommendation
- Include key numbers/metrics
- End with primary action items

**Example:**
```markdown
## Executive Summary

We analyzed **1,472 story submissions** from NJ News Commons members to identify the strongest candidates for the 2026 Excellence in NJ Local News Awards. Using specialized evaluation agents that read and assessed full article content, we identified **40+ top candidates** across all award categories.

### Key Findings

1. **Exceptional investigative journalism** from hyperlocal outlets rivals work from much larger newsrooms
2. **Ethnic media produced outstanding work** that was initially inaccessible
3. **Sustained coverage series** demonstrate accountability journalism at its best
```

### Key Findings
- Use numbered lists for priority/sequence
- Use bullet points for unordered findings
- **Bold key phrases** for scannability
- Include specific numbers when available
- Keep to 3-7 items (more requires subdivision)

### Recommendations Sections
**Tier structure approach:**
```markdown
## TOP RECOMMENDATIONS

### TIER 1: Must Prioritize (Highest Impact)

These 5 actions represent critical priorities:

1. **Action Item** - Specific description with rationale
2. **Action Item** - Specific description with rationale

### TIER 2: Strong Candidates (Medium Priority)

These 3 actions should follow Tier 1:

1. **Action Item** - Specific description with rationale
```

### Methodology Section
Include when the report involves:
- Data analysis
- Evaluation criteria
- Research process
- Scoring systems

**Structure:**
```markdown
## Methodology

### Evaluation Process

1. **Initial Review:** Description of first stage
2. **Analysis Phase:** Description of analysis methods
3. **Scoring Criteria:**
   - Criterion 1: Description
   - Criterion 2: Description
4. **Validation:** Description of quality checks

### Scoring Scale

- **10/10:** Exceptional - among the best produced anywhere
- **9/10:** Outstanding - clear award-worthy quality
- **8/10:** Strong - deserves serious consideration
- **7/10:** Good - honorable mention candidate
```

### Action Items / Next Steps
Use checkbox format for trackable tasks:

```markdown
## Timeline: Action Plan

### Week 1 (Jan 6-10): Immediate Actions
- [ ] Send follow-up emails to prospects
- [ ] NEW outreach to priority contacts
- [ ] Schedule planning meeting

### Week 2 (Jan 13-17): Follow-Up
- [ ] Phone calls to non-responders
- [ ] Submit applications
- [ ] Prepare proposals
```

---

## Text Formatting Conventions

### Emphasis
- **Bold** for key terms, important findings, emphasis
- *Italic* for titles of publications, foreign words, or subtle emphasis
- `Code formatting` for technical terms, commands, or inline references to tools

### Lists
**Bullet points:**
- Use `-` for bullets (not `*` or `+`)
- Maintain consistent indentation (2 or 4 spaces)
- Use sentence fragments or full sentences (be consistent)
- Capitalize first word
- End with period if full sentence, no period if fragment

**Numbered lists:**
- Use for sequential steps, priorities, or rankings
- Maintain number sequence (don't restart)
- Can use sub-numbers (1.1, 1.2) for nested items

### Links
```markdown
[Link text](https://example.com)
[Title of Article](https://example.com/article)
```

**Link conventions:**
- Use descriptive link text (not "click here")
- Include full URLs in reference sections
- For story links, use story title as link text

### Quotes and Callouts
```markdown
**Key Quote:** "Exact quote here" - Attribution

> Blockquote for longer excerpts or emphasis
> Can span multiple lines
```

---

## Special Elements

### Status Indicators
Use emoji or symbols for quick visual scanning:

**Status:**
- ✅ Complete / Approved / Yes
- ❌ Incomplete / Rejected / No
- ⏳ In Progress / Pending
- 🔄 Under Review
- ⚠️ Warning / Attention Needed

**Priority:**
- 🔴 HIGH / URGENT
- 🟡 MEDIUM
- 🟢 LOW
- ⚫ SKIP / NOT APPLICABLE

**Quality/Fit:**
- ⭐⭐⭐⭐⭐ Excellent
- ⭐⭐⭐⭐ Very Good
- ⭐⭐⭐ Good
- ⭐⭐ Fair
- ⭐ Poor

### Images
When including images:
```markdown
![Descriptive alt text](https://example.com/image.png)
```

Place images:
- At top of document (header images)
- Inline with relevant sections
- In appendices for supplementary visuals

### Code Blocks
For examples, templates, or technical content:
````markdown
```markdown
# Example template
Your content here
```
````

---

## Report Type Templates

### Template 1: Research Report

```markdown
# [Topic] Research Report

**Prepared for:** Organization
**Analysis Date:** Month Day, Year
**Prepared by:** Author Name

---

## Executive Summary

[2-3 paragraphs summarizing key findings and recommendations]

### Key Findings

1. **Finding 1** - Brief description
2. **Finding 2** - Brief description
3. **Finding 3** - Brief description

---

## Detailed Findings

### Category 1: [Name]

[Narrative explanation with data]

| Metric | Value | Analysis |
|--------|-------|----------|
| Data 1 | 100 | Description |
| Data 2 | 200 | Description |

### Category 2: [Name]

[Narrative explanation with data]

---

## Recommendations

### Priority 1: Immediate Actions

1. **Action** - Rationale and expected outcome
2. **Action** - Rationale and expected outcome

### Priority 2: Medium-Term Actions

1. **Action** - Rationale and expected outcome

---

## Methodology

### Research Process

1. **Data Collection:** Description
2. **Analysis Methods:** Description
3. **Validation:** Description

---

## Next Steps

- [ ] Action item 1
- [ ] Action item 2
- [ ] Action item 3

---

## References

- [Source 1](https://example.com)
- [Source 2](https://example.com)

---

*Report prepared [Date] for [Organization]*
```

### Template 2: Evaluation Report

```markdown
# [Program/Project] Evaluation Report
## [Subtitle if needed]

**Prepared for:** Organization
**Analysis Date:** Month Day, Year
**Prepared by:** Evaluation Team

---

## Executive Summary

We evaluated **[number]** [items] to [purpose]. Key findings reveal [major takeaway].

### Key Findings

1. **Finding 1** - Supporting data
2. **Finding 2** - Supporting data
3. **Finding 3** - Supporting data

---

## TOP RECOMMENDATIONS

### TIER 1: Must Recognize (Highest Scores)

These [number] [items] represent the best [category]:

| Rank | Item | Organization | Score | Category |
|------|------|--------------|-------|----------|
| 1 | Name | Org | 10/10 | Cat |
| 2 | Name | Org | 9.5/10 | Cat |

---

### TIER 2: Strong Candidates (Scores X-Y)

[Description of second tier]

| Item | Organization | Key Strength |
|------|--------------|--------------|
| Name | Org | Description |
| Name | Org | Description |

---

## Detailed Analysis

### Category 1: [Name]

[Narrative analysis]

**Standout examples:**
- **Item 1** - Why it excels
- **Item 2** - Why it excels

### Category 2: [Name]

[Narrative analysis]

---

## Methodology

### Evaluation Process

1. **Initial Review:** [Process]
2. **Scoring Phase:** [Process]
3. **Validation:** [Process]

### Scoring Criteria

- **Criterion 1:** Description
- **Criterion 2:** Description
- **Criterion 3:** Description

### Scoring Scale

- **10/10:** Exceptional
- **9/10:** Outstanding
- **8/10:** Strong
- **7/10:** Good

---

## Conclusion

[2-3 paragraphs synthesizing findings and emphasizing key recommendations]

---

## Appendix: [Name]

[Supplementary information]

---

*Report prepared [Date] for [Organization]*
```

### Template 3: Sponsorship/Partnership Report

```markdown
# [Event/Program] - Sponsorship Outreach Report

**Event Date:** Month Day, Year
**Report Generated:** Month Day, Year
**Time to Event:** X weeks

---

## Executive Summary

This report consolidates research on [number] prospective sponsors for [event/program]. Based on comprehensive analysis, we've identified **[number] high-priority prospects** to actively pursue, **[number] medium-priority prospects**, and **[number] to deprioritize**.

### Official Sponsorship Tiers ([Year] [Program])

| Tier | Price | Description | Key Benefits |
|------|-------|-------------|--------------|
| **Top Tier** | $X,XXX | Description | Benefit 1, Benefit 2, Benefit 3 |
| **Mid Tier** | $X,XXX | Description | Benefit 1, Benefit 2 |
| **Lower Tier** | $XXX | Description | Benefit 1, Benefit 2 |

**Contact:** Name, email@example.com

---

### Quick Reference: Sponsor Priority Matrix

| Priority | Organization | Status | Fit | Recommended Tier | Action Required |
|----------|-------------|--------|-----|------------------|-----------------|
| 🔴 HIGH | Org Name | Status | ⭐⭐⭐⭐⭐ | Tier ($X,XXX) | Action |
| 🟡 MED | Org Name | Status | ⭐⭐⭐ | Tier ($XXX) | Action |

---

## Priority 1: Immediate Follow-Up Required

### 1. Organization Name ⭐⭐⭐⭐⭐

**Status:** Current status
**Fit Rating:** EXCELLENT
**Recommended Ask:** Tier name ($amount)

**Why They're Perfect:**
- Reason 1 with specific evidence
- Reason 2 with specific evidence
- Reason 3 with specific evidence

**Key Contacts:**
| Name | Title | Contact |
|------|-------|---------|
| Name | Title | email@example.com |
| Name | Title | (555) 555-5555 |

**Follow-Up Strategy:**
1. Week 1: Action
2. Week 2: Action
3. Week 3: Action

**Talking Points:**
- "Point 1 that resonates with their mission"
- "Point 2 with specific data"
- "Point 3 connecting to their priorities"

---

[Repeat for each priority sponsor]

---

## Timeline: [Number]-Week Action Plan

### Week 1 ([Dates]): Immediate Actions
- [ ] Action item
- [ ] Action item
- [ ] Action item

### Week 2 ([Dates]): Follow-Up Phase
- [ ] Action item
- [ ] Action item

[Continue for all weeks until event]

---

## Official Sponsorship Tiers

### Top tier: $X,XXX
*Description of what this tier provides*
- Benefit 1
- Benefit 2
- Benefit 3

### Mid tier: $X,XXX
*Description of what this tier provides*
- Benefit 1
- Benefit 2

[Continue for all tiers]

---

## Projected Revenue Scenarios

### Conservative scenario ([number] sponsors)
| Sponsor | Tier | Amount |
|---------|------|--------|
| Org 1 | Tier | $X,XXX |
| Org 2 | Tier | $XXX |
| **TOTAL** | | **$X,XXX** |

### Moderate scenario ([number] sponsors)
[Similar table]

### Optimistic scenario ([number] sponsors)
[Similar table]

---

## Key Success Factors

### DO:
✅ Action 1
✅ Action 2
✅ Action 3

### DON'T:
❌ Anti-pattern 1
❌ Anti-pattern 2
❌ Anti-pattern 3

---

## Next Steps

1. **TODAY:** Action
2. **THIS WEEK:** Action
3. **ONGOING:** Action
4. **POST-EVENT:** Action

---

*Report compiled by [Organization/Team]*
*[Date]*
```

### Template 4: Concept Paper / Proposal

```markdown
![Optional header image](https://example.com/image.png)

# Concept Paper
### [Program Title]: [Subtitle]

### **Introduction**
[2-3 paragraphs setting context and introducing the problem]

### **The problem and our solution**
[Define the problem clearly, then present your solution]

**Problem statement:** [Specific problem you're solving]

**Solution:** [Your approach in 1-2 sentences]

## **How it would work**

[Overview paragraph]

### **Component 1**
[Description of first program component]

### **Component 2**
[Description of second program component]

[Continue for all components]

### **Example scenario:**
[Concrete example of how the program works in practice]

## **Who we would serve**
[Description of target audience/beneficiaries with specifics]

In Year 1, we would aim to [specific metrics]. The program would [scope description].

## **Why now**
[Urgency and timing rationale - 2-3 paragraphs]

## **Measuring success**
We would track program effectiveness through:

###  **Reach metrics:**
- Metric 1 (target: number by end of Year 1)
- Metric 2 (target: number per session)
- Metric 3 (target: number)

### **Outcome metrics:**
- Outcome 1
- Outcome 2
- Outcome 3

### **Quality metrics:**
- Quality measure 1
- Quality measure 2
- Quality measure 3

[Reporting cadence statement]

## **Beyond Year 1**

[Multi-year expansion plan]

### **Year 2 ($XXX,XXX):**
- Expansion 1
- Expansion 2
- Target: [metrics]

### **Year 3 ($XXX,XXX):**
- Expansion 1
- Expansion 2
- Target: [metrics]

## **Sustainability**

After the initial funding period, the program could sustain itself through:

- **Model 1:** Description
- **Model 2:** Description
- **Model 3:** Description

[Context on why sustainability is achievable]

## **Background on [Person/Team]**

[2-3 paragraphs on key personnel, qualifications, and relevant experience]

[Bulleted list of relevant projects/achievements with brief descriptions and links]

## **Background on [Organization]**

[Organization mission and track record - 2 paragraphs]

[Examples of similar programs or relevant experience:]

### **[Program 1]**
Description with impact

### **[Program 2]**
Description with impact

[Connection to proposed program]

## **Budget — Year 1**

| EXPENSE ITEM | AMOUNT |
| :---- | ----: |
| Category 1 (description) | $XX,XXX |
| Category 2 (description) | $XX,XXX |
| Category 3 (description) | $X,XXX |
| **TOTAL** | **$XXX,XXX** |

---

## **Publications and media**

[Organized by type]

### *Category 1:*
- [Publication 1](https://link.com) — Description
- [Publication 2](https://link.com) — Description

### *Category 2:*
- [Item 1](https://link.com) — Description
- [Item 2](https://link.com) — Description

---

## **References and resources**

[Organized by type with full links]

### *Category 1:*
- Resource 1: https://link.com
- Resource 2: https://link.com

### *Category 2:*
- Resource 1: https://link.com
- Resource 2: https://link.com
```

---

## Changelog Generation Patterns

When updates are made to reports, document them with a changelog section:

### Changelog Format
```markdown
## Changelog

### [Date] - [Version or Update Type]
**Changes:**
- Added [description]
- Updated [description]
- Removed [description]

**Rationale:** [Why changes were made]

### [Earlier Date] - [Update Type]
**Changes:**
- Change description

---
```

### Update Types
- **Major revision** - Substantial changes to findings or recommendations
- **Minor update** - Clarifications, corrections, or small additions
- **Data refresh** - Updated figures or metrics
- **Supplemental findings** - New information added
- **Formatting** - No content changes, only presentation

### Placement
- Place at beginning of document (after front matter, before Executive Summary) for active documents
- Place at end of document (before references) for archived reports

---

## Quality Checklist

Before finalizing any report, verify:

### Structure
- [ ] Front matter complete (title, metadata, separator)
- [ ] Executive Summary standalone and comprehensive
- [ ] Section headings hierarchical and descriptive
- [ ] Horizontal rules between major sections
- [ ] Conclusion or Next Steps section present

### Content
- [ ] Key findings numbered and bold
- [ ] Data/numbers included where relevant
- [ ] Specific, actionable recommendations
- [ ] Attribution for quotes and sources
- [ ] Methodology explained if evaluation/analysis

### Formatting
- [ ] Tables properly aligned (left for text, right for numbers)
- [ ] All links functional and descriptive
- [ ] Bold/italic used consistently for emphasis
- [ ] Lists formatted consistently (bullets vs. numbers)
- [ ] No orphaned sections (content under every heading)

### Tables
- [ ] Headers clear and descriptive
- [ ] Alignment appropriate for data type
- [ ] Totals rows bolded in budget tables
- [ ] Column widths reasonable (no excessive white space)
- [ ] All cells populated (no empty cells without reason)

### Professionalism
- [ ] Tone professional and clear
- [ ] No typos or grammatical errors
- [ ] Consistent terminology throughout
- [ ] Date and attribution at end
- [ ] Contact information included where appropriate

### Accessibility
- [ ] Headings create logical document outline
- [ ] Alt text for images included
- [ ] Link text descriptive (not "click here")
- [ ] Tables not overly complex (split if >7 columns)
- [ ] Color not sole conveyor of meaning (use text + symbols)

---

## Style Guide Quick Reference

### Capitalization
- **Report titles:** Title Case
- **Section headings:** Title Case or Sentence case (be consistent)
- **Table headers:** ALL CAPS for budget tables, Title Case for others
- **Organization names:** Follow official capitalization
- **Job titles:** Title Case when preceding name, lowercase otherwise

### Numbers
- Use numerals for numbers 10 and above
- Spell out numbers one through nine (except in tables/lists)
- Use commas for thousands (1,000 not 1000)
- Use $ symbol for currency ($1,000)
- Use percent symbol (75%)
- Use decimals for precision (9.5/10)

### Dates
- **Long form:** Month Day, Year (January 15, 2026)
- **Short form:** MM/DD/YYYY (01/15/2026)
- **Date ranges:** Jan 6-10 or January 6-10, 2026
- Be consistent within a document

### Contact Information
**Phone numbers:** (555) 123-4567 or 555-123-4567
**Emails:** firstname.lastname@domain.com (hyperlinked)
**URLs:** Full URL in reference sections, hyperlinked in-text

### Abbreviations
- Spell out on first use, then abbreviate: Center for Cooperative Media (CCM)
- Use standard abbreviations: vs. (versus), etc. (et cetera), e.g. (for example)
- No periods in acronyms: AARP, PBS, CNN

---

## When to Use Each Report Type

### Research Report
**Use when:**
- Investigating a question or topic
- Compiling information from multiple sources
- Providing background for decision-making
- No evaluation/scoring involved

**Examples:** Market research, literature reviews, feasibility studies

### Evaluation Report
**Use when:**
- Assessing quality or merit
- Scoring/ranking items
- Making recommendations based on criteria
- Judging competition entries

**Examples:** Award evaluations, program assessments, grant reviews

### Sponsorship/Partnership Report
**Use when:**
- Seeking funding or sponsorships
- Building partnerships
- Tracking outreach efforts
- Managing relationship pipeline

**Examples:** Event sponsorship, fundraising campaigns, collaboration development

### Concept Paper
**Use when:**
- Proposing new programs or initiatives
- Seeking grant funding
- Building case for organizational investment
- Pitching ideas to stakeholders

**Examples:** Grant applications, program proposals, pilot project pitches

---

## Advanced Formatting Techniques

### Multi-Column Layouts
For side-by-side comparisons:

```markdown
| Before | After |
|--------|-------|
| Old approach: Manual data entry taking 4 hours per report | New approach: Automated pipeline takes 10 minutes |
| Limited to 50 records per analysis | Can process 10,000+ records |
| Error rate: 5-7% | Error rate: <0.1% |
```

### Nested Lists
For hierarchical information:

```markdown
1. **Primary category**
   - Subcategory A
     - Detail 1
     - Detail 2
   - Subcategory B
2. **Second category**
   - Subcategory C
```

### Definition Lists
For terminology or glossary sections:

```markdown
**Term 1**
: Definition or explanation of the term

**Term 2**
: Definition or explanation with multiple lines
: Can continue on subsequent lines with colon prefix
```

### Inline HTML (use sparingly)
For complex tables or specific formatting needs:
```html
<table>
  <tr>
    <th>Header</th>
  </tr>
  <tr>
    <td>Data</td>
  </tr>
</table>
```

---

## Common Mistakes to Avoid

### Table Formatting
❌ **Wrong:**
```markdown
|Name|Email|
|---|---|
|Jane|jane@email.com|
```
Missing spaces, hard to read

✅ **Correct:**
```markdown
| Name | Email |
|------|-------|
| Jane | jane@email.com |
```

### List Formatting
❌ **Wrong:**
```markdown
- item 1
-item 2
  - nested without proper parent
```

✅ **Correct:**
```markdown
- Item 1
- Item 2
  - Nested under Item 2
  - Another nested item
```

### Heading Hierarchy
❌ **Wrong:**
```markdown
# Title
### Skipped Level 2
## Back to Level 2
```

✅ **Correct:**
```markdown
# Title
## Level 2
### Level 3
## Another Level 2
```

### Link Formatting
❌ **Wrong:**
```markdown
Click here: https://example.com
[click here](https://example.com)
```

✅ **Correct:**
```markdown
[Descriptive Link Text](https://example.com)
Visit the [2026 Annual Report](https://example.com/report)
```

### Emphasis Overload
❌ **Wrong:**
```markdown
**This is a *very* important finding that shows ***significant*** results**
```

✅ **Correct:**
```markdown
This is a **very important finding** that shows significant results
```

---

## Report Writing Best Practices

### Executive Summary
- **Write last** - After completing the full report
- **Can stand alone** - Reader should understand key points without reading further
- **Include numbers** - Specific metrics more compelling than generalizations
- **Lead with action** - What should reader do with this information?

### Section Flow
- **Logical progression** - Each section builds on previous
- **Topic sentences** - First sentence of paragraph states main point
- **Transitions** - Connect ideas between paragraphs and sections
- **Parallel structure** - Similar items formatted similarly

### Data Presentation
- **Tables for comparison** - Side-by-side data
- **Bullet points for lists** - 3-7 related items
- **Numbered lists for steps** - Sequential or prioritized information
- **Narrative for context** - Explain what the data means

### Recommendations
- **Specific and actionable** - Clear what needs to happen
- **Prioritized** - Not all recommendations equal importance
- **Owner identified** - Who should take action
- **Timeline indicated** - When action should occur
- **Rationale provided** - Why this recommendation matters

---

## Tools and Workflow

### Before Writing
1. **Identify report type** - Which template applies?
2. **Gather all data** - Collect sources, numbers, contacts
3. **Outline structure** - Adapt template to your needs
4. **Define audience** - Who will read and use this?

### During Writing
1. **Start with body** - Write main content first
2. **Create tables early** - Visualize data as you analyze
3. **Track sources** - Note links and citations as you go
4. **Use consistent formatting** - Apply standards throughout

### After Writing
1. **Write executive summary** - Distill key points
2. **Review structure** - Check heading hierarchy
3. **Verify tables** - Test alignment, check totals
4. **Proofread** - Check spelling, grammar, consistency
5. **Run quality checklist** - Verify all standards met
6. **Get feedback** - Have colleague review before finalizing

### Maintenance
1. **Version control** - Date updates, track changes
2. **Update changelogs** - Document what changed and why
3. **Archive old versions** - Keep record of iterations
4. **Share templates** - Make formatting standards accessible

---

## Example Use Cases

### Converting Research Notes to Report
**Input:** Raw research notes, web links, scattered findings

**Process:**
1. Choose Research Report template
2. Organize findings by theme into sections
3. Create summary table of sources
4. Extract key findings (3-5 bullet points)
5. Write executive summary
6. Add front matter and references
7. Run quality checklist

**Output:** Professional research report with clear structure

### Formatting Evaluation Results
**Input:** Scoring spreadsheet, notes on evaluated items

**Process:**
1. Choose Evaluation Report template
2. Create ranking table (top tier)
3. Build comparison tables (second tier)
4. Write narrative analysis for each category
5. Document methodology and scoring criteria
6. Add recommendations based on findings
7. Format and proofread

**Output:** Evaluation report with tiered recommendations

### Building Sponsorship Proposal
**Input:** List of prospects, research on each, sponsorship tiers

**Process:**
1. Choose Sponsorship Report template
2. Create priority matrix table
3. Write detailed profile for each prospect (use standard format)
4. Build timeline with action items
5. Add talking points for outreach
6. Include revenue scenarios
7. Format contact tables consistently

**Output:** Actionable sponsorship outreach report

---

## Skill Usage Instructions

When user requests report formatting assistance:

1. **Identify report type** - Ask if not clear from context
2. **Provide appropriate template** - Full template from this skill
3. **Adapt to specific needs** - Customize sections as needed
4. **Explain formatting choices** - Reference standards from this skill
5. **Review final output** - Check against quality checklist

When converting raw research to formatted report:

1. **Analyze content** - Identify themes, priorities, key findings
2. **Select template** - Match to report purpose
3. **Organize information** - Map content to template sections
4. **Format tables** - Apply appropriate alignment and structure
5. **Write executive summary** - Distill essence for busy readers
6. **Polish** - Apply all formatting standards

When user shows example or asks about specific formatting:

1. **Reference this skill** - Cite relevant section
2. **Show correct format** - Provide code block example
3. **Explain rationale** - Why this convention matters
4. **Suggest alternatives** - When multiple valid approaches exist

---

## References and Resources

### CCM Report Examples
- `/home/user/ccm/reports/2026-2028 AI support for local news organizations.md` - Concept paper format
- `/home/user/ccm/reports/ELN/2026-ELN-Final-Report.md` - Evaluation report format
- `/home/user/ccm/reports/ecm-sponsorship-2026/ECM-SPONSORSHIP-MASTER-REPORT.md` - Sponsorship report format

### Markdown Resources
- Basic syntax guide: https://www.markdownguide.org/basic-syntax/
- Extended syntax: https://www.markdownguide.org/extended-syntax/
- GitHub Flavored Markdown: https://github.github.com/gfm/

### Report Writing Resources
- [Add CCM-specific resources as available]

---

*Report Formatting Skill v1.0*
*Center for Cooperative Media*
*Last updated: January 2026*
