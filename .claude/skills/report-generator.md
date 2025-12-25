# Research Report Generator

Create interactive web reports from analysis data. Use when building dashboards or research presentations.

## You Are

A CCM researcher who has built the NJ Influencer research report. You know the exact theme system, Chart.js integration, and interactive features that make reports engaging.

## Report Structure

```
reports/
└── {project}-deploy/
    ├── index.html          # Main interactive report
    ├── research-brief.html # Academic format
    └── videos/             # Self-hosted media
```

## Theme System

CSS custom properties with dark mode:
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
}
```

Toggle implementation:
```javascript
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateChartColors(next);
}

// Initialize from preference
const saved = localStorage.getItem('theme') ||
  (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
document.documentElement.setAttribute('data-theme', saved);
```

## Animated Stat Counters

```javascript
function animateCounter(element, target, duration = 2000) {
  const start = 0;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = Math.floor(start + (target - start) * eased);
    element.textContent = current.toLocaleString();

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

## Chart.js Integration

Theme-aware charts:
```javascript
const chartColors = {
  light: {
    text: '#1a1a1a',
    grid: '#e5e7eb',
    primary: '#CA3553',
    secondary: '#2A9D8F'
  },
  dark: {
    text: '#f5f5f5',
    grid: '#404040',
    primary: '#e85d75',
    secondary: '#3dbdac'
  }
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
  Chart.helpers.each(Chart.instances, (chart) => {
    // Update colors and re-render
    chart.options.plugins.legend.labels.color = chartColors[theme].text;
    chart.update();
  });
}
```

## Common Chart Types

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
    labels: topTopics.map(t => t.name),
    datasets: [{ data: topTopics.map(t => t.count), backgroundColor: '#CA3553' }]
  },
  options: { indexAxis: 'y' }
});
```

## Section Template

```html
<section id="findings" class="py-16">
  <div class="max-w-6xl mx-auto px-4">
    <h2 class="text-3xl font-serif font-bold mb-8" style="color: var(--text)">
      Key Findings
    </h2>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div class="p-6 rounded-lg" style="background: var(--card)">
        <div class="stat-counter text-4xl font-bold" data-value="3650" style="color: var(--accent)">0</div>
        <div class="text-sm mt-2" style="color: var(--text); opacity: 0.7">Posts Analyzed</div>
      </div>
      <!-- More stat cards -->
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

## Video Embedding

Self-host videos for reliability:
```html
<video controls class="w-full rounded-lg">
  <source src="videos/case-study-1.mp4" type="video/mp4">
</video>
```

Fallback for embedded iframes:
```javascript
document.querySelectorAll('iframe').forEach(iframe => {
  iframe.onerror = () => {
    iframe.outerHTML = `<div class="p-4 bg-gray-100 rounded">Video unavailable. <a href="${iframe.src}">View on platform</a></div>`;
  };
});
```

## Copy-to-Clipboard

```javascript
function copyToClipboard(text, button) {
  navigator.clipboard.writeText(text).then(() => {
    const original = button.textContent;
    button.textContent = 'Copied!';
    setTimeout(() => button.textContent = original, 2000);
  });
}
```

## Output Location

Save to `/social-scraper/reports/{project}-deploy/` or `/reports/`
