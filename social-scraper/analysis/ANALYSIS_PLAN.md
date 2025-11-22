# NJ Influencer Analysis Plan

## Overview
Once Instagram batch 4 completes, we'll have scraped data from all 39 NJ influencers across three platforms. This document outlines the steps to consolidate, analyze, and generate reports from this data.

---

## Phase 1: Data Consolidation

### Run the Consolidation Script
```bash
cd analysis
python3 consolidate.py
```

This will:
- Parse all JSON metadata from TikTok, YouTube, and Instagram
- Calculate per-influencer metrics across all platforms
- Export consolidated CSVs to `analysis/data/`

### Expected Output Files
```
analysis/data/
├── all_posts.csv              # Every post from all platforms
├── influencer_metrics.csv     # Aggregated metrics per influencer
├── tiktok_posts.csv           # TikTok-specific data
├── youtube_posts.csv          # YouTube-specific data
├── instagram_posts.csv        # Instagram-specific data
└── summary.json               # High-level statistics
```

### Estimated Data Volume
| Platform | Posts | Views | Engagement |
|----------|-------|-------|------------|
| TikTok | ~1,450 | 209M+ | 21M+ |
| YouTube | ~150 | 33M+ | 900K+ |
| Instagram | ~1,950 | TBD | TBD |
| **Total** | **~3,550** | **240M+** | **22M+** |

---

## Phase 2: Run Analysis Notebook

### Install Dependencies
```bash
pip install -r analysis/requirements.txt
```

### Launch Jupyter
```bash
cd analysis
jupyter notebook nj_influencer_analysis.ipynb
```

### Notebook Sections
1. **Data Loading** - Load consolidated CSVs
2. **Ecosystem Overview** - Platform distribution, total metrics
3. **Influence Rankings** - Top influencers by engagement
4. **Content Analysis** - Categorization by topic (News, Sports, Food, etc.)
5. **Temporal Analysis** - Posting patterns over time
6. **Ecosystem Map** - Platform activity heatmap
7. **Key Findings Summary** - Executive summary

---

## Phase 3: Generated Outputs

### Visualizations (saved to `analysis/figures/`)
- `platform_overview.png` - Posts and engagement by platform
- `top_influencers.png` - Top 20 by total engagement
- `platform_breakdown.png` - Platform-specific engagement for top 10
- `engagement_rate.png` - Engagement rate vs total views
- `content_categories.png` - Posts and engagement by category
- `temporal_activity.png` - Posting activity over time
- `ecosystem_heatmap.png` - Platform activity matrix
- `platform_specialization.png` - Primary platforms pie chart

### Data Exports
- `all_posts_categorized.csv` - Posts with content categories
- `influencer_metrics_updated.csv` - Metrics with primary platform

---

## Phase 4: Research Report

### Key Questions to Answer
1. **Who are the most influential NJ content creators?**
   - Ranked by total engagement, views, follower reach

2. **What platforms dominate the NJ influencer landscape?**
   - TikTok vs Instagram vs YouTube distribution

3. **What content categories are most prevalent?**
   - News/Politics, Sports, Food, Lifestyle, Entertainment, Local/Community

4. **What's the engagement rate across platforms?**
   - Which platform drives highest engagement per view?

5. **Who are the top influencers in each category?**
   - News influencers, Sports influencers, Food influencers, etc.

### Report Structure
1. Executive Summary
2. Methodology
3. Ecosystem Overview
4. Platform Analysis
5. Influence Rankings
6. Content Categorization
7. Key Findings
8. Recommendations

---

## Quick Start Commands

```bash
# 1. Navigate to analysis directory
cd /Users/jamditis/Desktop/Crimes/playground/social-scraper/analysis

# 2. Run consolidation
python3 consolidate.py

# 3. Install notebook dependencies (if needed)
pip install pandas matplotlib seaborn jupyter

# 4. Launch notebook
jupyter notebook nj_influencer_analysis.ipynb
```

---

## Timeline

| Step | Task | Duration |
|------|------|----------|
| 1 | Instagram batch 4 completes | ~45 min |
| 2 | Run consolidation script | ~2 min |
| 3 | Execute analysis notebook | ~5 min |
| 4 | Review visualizations | ~10 min |
| 5 | Generate final report | ~30 min |

**Total estimated time after batch 4:** ~1 hour

---

## Notes

- The content categorization is keyword-based and may need manual refinement
- Some influencers may have missing data if scraping failed
- Engagement rates vary significantly by platform norms
- Consider adding follower counts for normalized influence scores (requires additional API calls)
