"""
Visualization Library Comparison
Compare matplotlib/seaborn vs plotnine vs altair

Install requirements:
    pip install plotnine altair altair_saver vl-convert-python
"""

import pandas as pd
import numpy as np

# Sample data (simulating influencer metrics)
np.random.seed(42)
data = pd.DataFrame({
    'influencer': [f'Influencer {i}' for i in range(1, 11)],
    'platform': np.random.choice(['TikTok', 'YouTube', 'Instagram'], 10),
    'followers': np.random.randint(10000, 500000, 10),
    'engagement': np.random.randint(1000, 50000, 10),
    'posts': np.random.randint(10, 50, 10)
})

# Sort for better visualization
data = data.sort_values('engagement', ascending=True)

print("=" * 60)
print("VISUALIZATION LIBRARY COMPARISON")
print("=" * 60)

# =============================================================================
# 1. MATPLOTLIB + SEABORN (Current approach)
# =============================================================================
print("\n1. Creating matplotlib/seaborn chart...")

import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=data, y='influencer', x='engagement', hue='platform', ax=ax)
ax.set_title('Top Influencers by Engagement', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Engagement')
ax.set_ylabel('')
ax.legend(title='Platform', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig('figures/comparison_seaborn.png', dpi=150, bbox_inches='tight')
plt.close()
print("   Saved: figures/comparison_seaborn.png")


# =============================================================================
# 2. PLOTNINE (ggplot2 syntax in Python)
# =============================================================================
print("\n2. Creating plotnine chart...")

try:
    from plotnine import (
        ggplot, aes, geom_col, coord_flip, theme_minimal,
        labs, theme, element_text, scale_fill_brewer
    )

    p = (
        ggplot(data, aes(x='influencer', y='engagement', fill='platform'))
        + geom_col()
        + coord_flip()
        + theme_minimal()
        + labs(
            title='Top Influencers by Engagement',
            x='',
            y='Total Engagement',
            fill='Platform'
        )
        + scale_fill_brewer(type='qual', palette='Set2')
        + theme(
            plot_title=element_text(size=14, weight='bold'),
            figure_size=(10, 6)
        )
    )

    p.save('figures/comparison_plotnine.png', dpi=150)
    print("   Saved: figures/comparison_plotnine.png")

except ImportError:
    print("   Plotnine not installed. Run: pip install plotnine")


# =============================================================================
# 3. ALTAIR (Declarative, Vega-Lite based)
# =============================================================================
print("\n3. Creating altair chart...")

try:
    import altair as alt

    chart = alt.Chart(data).mark_bar().encode(
        y=alt.Y('influencer:N', sort='-x', title=''),
        x=alt.X('engagement:Q', title='Total Engagement'),
        color=alt.Color('platform:N',
                       scale=alt.Scale(scheme='set2'),
                       legend=alt.Legend(title='Platform'))
    ).properties(
        title='Top Influencers by Engagement',
        width=500,
        height=300
    ).configure_title(
        fontSize=14,
        fontWeight='bold'
    )

    chart.save('figures/comparison_altair.png', scale_factor=2)
    print("   Saved: figures/comparison_altair.png")

except ImportError:
    print("   Altair not installed. Run: pip install altair vl-convert-python")
except Exception as e:
    print(f"   Altair error: {e}")
    print("   Try: pip install vl-convert-python")


# =============================================================================
# 4. R ggplot2 equivalent (for reference)
# =============================================================================
print("\n4. R ggplot2 equivalent code (for reference):")
print("""
   library(tidyverse)

   ggplot(data, aes(x = reorder(influencer, engagement),
                    y = engagement,
                    fill = platform)) +
     geom_col() +
     coord_flip() +
     theme_minimal() +
     labs(title = "Top Influencers by Engagement",
          x = "",
          y = "Total Engagement",
          fill = "Platform") +
     scale_fill_brewer(palette = "Set2")
""")

print("\n" + "=" * 60)
print("COMPARISON SUMMARY")
print("=" * 60)
print("""
Code Verbosity (lines for same chart):
  - R ggplot2:    ~10 lines
  - Plotnine:     ~15 lines
  - Altair:       ~15 lines
  - Seaborn:      ~10 lines (but more tweaking needed)

Output Quality:
  - R ggplot2:    ★★★★★ (best defaults)
  - Altair:       ★★★★☆ (very clean)
  - Plotnine:     ★★★★☆ (good, matplotlib-based)
  - Seaborn:      ★★★☆☆ (needs work)

Recommendation for your project:
  → Use Altair for clean, publication-ready static charts
  → Plotnine if you want ggplot2 syntax
  → Seaborn is fine for quick exploration
""")

print("\nCheck the figures/ directory to compare outputs!")
