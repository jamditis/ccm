# Research Report Generator

---
description: Create interactive web reports with dark mode, animated stats, and Chart.js visualizations
activation_triggers:
  - "create a report"
  - "build dashboard"
  - "interactive visualization"
  - "research report"
  - "publish findings"
related_skills:
  - research-pipeline
  - content-analyzer
---

## When to Use

- Creating interactive HTML reports from research data
- Building dashboards with Chart.js visualizations
- Publishing findings with dark/light mode support
- Need animated stat counters and theme-aware charts

## When NOT to Use

- Generating static images (use `generate_visualizations.py` directly)
- Building journalism tools (use journalism-tool-builder)
- Creating PDFs (use html2pdf.js in tools, not reports)

## You Are

A CCM researcher who built the NJ Influencer report. You know the exact theme system, Chart.js patterns, and how to make data engaging. You've shipped a report with 3,650 posts analyzed and self-hosted video embeds.

## Report Structure

```
reports/
└── {project}-deploy/
    ├── index.html          # Main interactive report
    ├── research-brief.html # Academic format (optional)
    └── videos/             # Self-hosted media
```

## Theme System

CSS custom properties with dark mode support:

```css
:root {
  --bg: #ffffff;
  --card: #f8f9fa;
  --text: #1a1a1a;
  --border: #e5e7eb;
  --accent: #CA3553;
}

[data-theme="dark"] {
  --bg: #1a1a1a;
  --card: #2d2d2d;
  --text: #f5f5f5;
  --border: #404040;
  --accent: #e85d75;
}

body {
  background: var(--bg);
  color: var(--text);
  transition: background 0.3s, color 0.3s;
}
```

Theme toggle with persistence:

```javascript
function initTheme() {
  const saved = localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateChartColors(next);
}

initTheme();
```

## Animated Stat Counters

```javascript
function animateCounter(element, target, duration = 2000) {
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);  // ease-out cubic
    element.textContent = Math.floor(target * eased).toLocaleString();

    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// Trigger on scroll into view
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounter(entry.target, parseInt(entry.target.dataset.value));
      observer.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('.stat-counter').forEach(el => observer.observe(el));
```

HTML for stat cards:
```html
<div class="stat-counter text-4xl font-bold" data-value="3650" style="color: var(--accent)">0</div>
<div class="text-sm opacity-70">Posts Analyzed</div>
```

## Theme-Aware Chart.js

```javascript
const chartColors = {
  light: { text: '#1a1a1a', grid: '#e5e7eb', primary: '#CA3553', secondary: '#2A9D8F' },
  dark: { text: '#f5f5f5', grid: '#404040', primary: '#e85d75', secondary: '#3dbdac' }
};

function createChart(ctx, type, data, options = {}) {
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  const colors = chartColors[theme];

  return new Chart(ctx, {
    type,
    data,
    options: {
      ...options,
      plugins: {
        legend: { labels: { color: colors.text } }
      },
      scales: type !== 'pie' && type !== 'doughnut' ? {
        x: { ticks: { color: colors.text }, grid: { color: colors.grid } },
        y: { ticks: { color: colors.text }, grid: { color: colors.grid } }
      } : undefined
    }
  });
}

function updateChartColors(theme) {
  const colors = chartColors[theme];
  Chart.helpers.each(Chart.instances, (chart) => {
    chart.options.plugins.legend.labels.color = colors.text;
    if (chart.options.scales) {
      chart.options.scales.x.ticks.color = colors.text;
      chart.options.scales.y.ticks.color = colors.text;
    }
    chart.update();
  });
}
```

## Common Chart Patterns

**Sentiment Distribution (Pie):**
```javascript
new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [{
      data: [45, 35, 20],
      backgroundColor: ['#22c55e', '#6b7280', '#ef4444']
    }]
  }
});
```

**Topic Breakdown (Horizontal Bar):**
```javascript
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: topics.map(t => t.name),
    datasets: [{ data: topics.map(t => t.count), backgroundColor: '#CA3553' }]
  },
  options: { indexAxis: 'y' }
});
```

**Correlation Scatter:**
```javascript
new Chart(ctx, {
  type: 'scatter',
  data: {
    datasets: [{
      data: posts.map(p => ({ x: p.sentiment, y: p.authenticity })),
      backgroundColor: posts.map(p => p.controversy > 0.7 ? '#ef4444' : '#CA3553')
    }]
  }
});
```

## Section Template

```html
<section id="findings" class="py-16">
  <div class="max-w-6xl mx-auto px-4">
    <h2 class="text-3xl font-serif font-bold mb-8" style="color: var(--text)">
      Key Findings
    </h2>

    <!-- Stat Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div class="p-6 rounded-lg" style="background: var(--card)">
        <div class="stat-counter text-4xl font-bold" data-value="3650">0</div>
        <div class="text-sm mt-2 opacity-70">Posts Analyzed</div>
      </div>
    </div>

    <!-- Chart -->
    <div class="p-6 rounded-lg" style="background: var(--card)">
      <canvas id="sentimentChart"></canvas>
    </div>
  </div>
</section>
```

## Typography

```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">

<style>
  h1, h2, h3 { font-family: 'Cormorant Garamond', serif; }
  body { font-family: 'DM Sans', sans-serif; }
</style>
```

## Self-Hosted Videos

Embed platforms often fail (403 errors). Self-host for reliability:

```html
<video controls class="w-full rounded-lg" poster="videos/thumbnail.jpg">
  <source src="videos/case-study-1.mp4" type="video/mp4">
  Your browser does not support video.
</video>
```

Total video budget: ~33 MB for 8 case studies in NJ Influencer report.

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip theme system | Users expect dark mode | Always implement CSS variables |
| Use static chart colors | Charts invisible in dark mode | Use theme-aware colors |
| Embed TikTok/Instagram directly | 403 errors, slow loading | Self-host videos |
| Forget IntersectionObserver | Counters animate off-screen | Trigger on scroll into view |
| Hard-code numbers | Can't update easily | Use data-value attributes |

## Output

Save to: `/social-scraper/reports/{project}-deploy/` or `/reports/`
